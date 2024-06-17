package main

import (
	"fmt"
	"github.com/BurntSushi/toml"
	"github.com/adrg/postcode"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/sqs"
	"github.com/gorilla/mux"
	"io/ioutil"
	"log"
	"net/http"
)

type (
	Config struct {
		QueueURL string `toml:"queue_url"`
	}
)

var (
	config Config
)

func postcodeHandler(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	if err := postcode.Validate(vars["postcode"]); err != nil {
		w.WriteHeader(http.StatusBadRequest)
	} else {
		w.WriteHeader(http.StatusOK)
		sendPostcodeToSQS(vars["postcode"])
	}
}

func sendPostcodeToSQS(p string) {
	sess := session.Must(session.NewSessionWithOptions(session.Options{
		SharedConfigState: session.SharedConfigEnable,
	}))
	svc := sqs.New(sess)
	result, err := svc.SendMessage(&sqs.SendMessageInput{
		DelaySeconds: aws.Int64(10),
		MessageAttributes: map[string]*sqs.MessageAttributeValue{
			"Postcode": &sqs.MessageAttributeValue{
				DataType:    aws.String("String"),
				StringValue: aws.String(p),
			},
		},
		QueueUrl: &config.QueueURL,
	})

	if err != nil {
		fmt.Println("Error", err)
		return
	}

	fmt.Println("Success", *result.MessageId)
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
	r := mux.NewRouter()
	r.HandleFunc("/postcode/{postcode}", postcodeHandler)
	err := http.ListenAndServe(":8080", r)
	if err != nil {
		log.Printf("Could not start postcode-api: %s", err.Error())
	}
}
