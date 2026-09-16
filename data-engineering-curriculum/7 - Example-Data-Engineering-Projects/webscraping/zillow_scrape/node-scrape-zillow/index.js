// https://blog.tericcabrel.com/how-to-scrape-zillow-nodejs/
// https://github.com/tericcabrel/blog-tutorials/tree/main/node-scrape-zillow?ref=blog.tericcabrel.com
// https://www.scrapingdog.com/blog/web-scraping-with-nodejs/
// https://nodemaven.com/
// https://github.com/apify/proxy-chain
// https://www.youtube.com/watch?v=Q5qkGq_Ustc
// how to create a proxy server in node js implementing custom logic part 1: https://www.youtube.com/watch?v=MCkKLVu1Y74

const unirest = require('unirest');
const cheerio = require('cheerio');
require('dotenv').config()
const fs = require('fs');
const { type } = require('os');

async function zillow() {
    const target_url = `https://api.scrapingdog.com/scrape?api_key=${process.env.API_KEY}&url=https://www.zillow.com/homes/modesto_rb/&dynamic=false&dynamic=false/`;
    const zillow_data = await unirest.get(target_url);

    const $ = cheerio.load(zillow_data.body);
    console.log("loading data")
    if (zillow_data.statusCode === 200) {
        console.log("success")
        // fs.writeFile('zillow_body.html', zillow_data.body, (err) => { 
          
        //     // In case of a error throw err. 
        //     if (err) throw err; 
        // })
        // let html = fs.readFileSync("zillow_body.html", "utf-8");

        let housesInfo = []
        $('article').each((index, element) => {
            const article = $(element);
          
            // Extract address
            const address = article.find('address[data-test="property-card-addr"]').text().trim();
          
            // Extract price
            const price = article.find('span[data-test="property-card-price"]').text().trim();
          
            // Extract bedrooms
            const bedrooms = article
              .find('ul.StyledPropertyCardHomeDetailsList-c11n-8-84-3__sc-1xvdaej-0 li')
              .filter((index, element) => $(element).text().includes('bds'))
              .find('b')
              .text();
          
            // Extract bathrooms
            const bathrooms = article
              .find('ul.StyledPropertyCardHomeDetailsList-c11n-8-84-3__sc-1xvdaej-0 li')
              .filter((index, element) => $(element).text().includes('ba'))
              .find('b')
              .text();
          
            // Extract square feet
            const squareFeet = article
              .find('ul.StyledPropertyCardHomeDetailsList-c11n-8-84-3__sc-1xvdaej-0 li')
              .filter((index, element) => $(element).text().includes('sqft'))
              .find('b')
              .text();
          
            housesInfo.push({
                    listing:index + 1,
                    address:address,
                    price:price,
                    bedrooms:bedrooms,
                    bathrooms:bathrooms,
                    squareFeet:squareFeet
                });
          });

        console.table(housesInfo);
        fs.writeFile(
            "homes.json",
            JSON.stringify(housesInfo),
            (err) => {
                if (err) throw err;
            }
        )
   } else{
    console.log(zillow_data.statusCode)
   }
}

zillow();