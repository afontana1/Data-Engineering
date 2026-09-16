package main

import (
	"fmt"
	"github.com/BurntSushi/toml"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/sqs"
	"io/ioutil"
	"log"
)

type (
	Config struct {
		QueueURL                       string `toml:"queue_url"`
		MaxConcurrentReceivedPostcodes int64  `toml:"max_concurrent_received_postcodes"`
		SQSWaitTimeSeconds             int64  `toml:"sqs_wait_time_seconds"`
	}

	Address struct {
		FirstLine  string
		SecondLine string
		Town       string
		Region     string
		Country    string
		Postcode   string
	}
)

var (
	config Config
)

func pollSQSForPostcode(svc *sqs.SQS, c chan<- *sqs.Message) {

	for {
		output, err := svc.ReceiveMessage(&sqs.ReceiveMessageInput{
			QueueUrl:            &config.QueueURL,
			MaxNumberOfMessages: aws.Int64(config.MaxConcurrentReceivedPostcodes),
			WaitTimeSeconds:     aws.Int64(config.SQSWaitTimeSeconds),
		})

		if err != nil {
			fmt.Errorf("failed to fetch sqs message %v", err)
		}

		for _, message := range output.Messages {
			c <- message
		}

	}

}

func lookupMatchingAddresses(msg *sqs.Message) (addresses []Address) {
	return nil
}

func deleteSQSMessage(msg *sqs.Message) {

}

func storeAddressesInDynamoDB(addresses []Address) {

}

func initConfig(path string) (appConfig Config) {
	tomlData, err := ioutil.ReadFile(path)
	if err != nil {
		log.Printf("Could not read config file: %s - %s", path, err.Error())
		return
	}
	_, err = toml.Decode(string(tomlData), &appConfig)
	if err != nil {
		log.Printf("Could not parse TOML config: %s - %s", path, err.Error())
	}
	return
}

func main() {
	config = initConfig("./config.toml")
	msgChan := make(chan *sqs.Message, config.MaxConcurrentReceivedPostcodes)
	sess := session.Must(session.NewSessionWithOptions(session.Options{
		SharedConfigState: session.SharedConfigEnable,
	}))
	svc := sqs.New(sess)
	go pollSQSForPostcode(svc, msgChan)

	fmt.Printf("Listening on stack queue: %s", config.QueueURL)

	for msg := range msgChan {
		results := lookupMatchingAddresses(msg)
		if len(results) > 0 {
			storeAddressesInDynamoDB(results)
		}
		deleteSQSMessage(msg)
	}
}
