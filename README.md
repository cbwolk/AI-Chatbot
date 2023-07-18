
# AI Slack Chatbot Project

#### By Colton Wolk

This project allows you to scrape Home Depot's website for product information and interact with a chatbot via Slack to answer questions about those products. The main files are `scraping.py` and `server.py`. The `requirements.txt` file lists necessary packages and `ProductList.csv` contains a list of nearly 700 products that have been scraped already. That list makes for a sufficient demonstration of how the chatbot works.

Note that some of the products listed in the sitemap are sold out, no longer available, or have other issues with their product pages. I filtered out product links that led to items without a name, but left others in. See [Future Work](#Future-Work).

## Running the bot

 **NOTE: Please contact me if you would like to test out the bot. I would be happy to add you to the Slack workspace and give you access to the proper files. Once you are set up, you may then follow the instructions below:**
 
 1. Ensure all packages in the `requirements.txt` file are installed.
 2. If you want to scrape the data yourself and regenerate `ProductList.csv`, run `scraping.py`. If not, continue to step 3. To save time, I modified the current code to scan only a few products (of the more than 13,000 in total). On my machine it took about 10 minutes to generate the list of nearly 700 products currently in `ProductList.csv`. 
 3. Run `server.py`. This starts the Flask app server on http 127.0.0.1:3000.
 4. Start the [Serveo](https://serveo.net) server that enables remote port forwarding. The link that is able to receive requests from Slack is [*redacted*]. In order to start the server, enter `ssh -R [redacted]:80:127.0.0.1:3000 serveo.net` into your terminal.
 5. Join the Slack workspace and start asking questions about Home Depot's products! You can interact with the bot by tagging @Product-Expert-ChatBot in the #chatbot-exercise channel. Join the Slack using this link: [*redacted*]

## Files

### `scraping.py`

The Home Depot sitemap is constructed in multiple layers. The parent link of all products is https://www.homedepot.com/sitemap/P/PIPs.xml, and there are two subcategories. In other words, this is how you get to a product page:

PIP XML link (above) --> XML link --> XML link --> Product page

In the file, I iterate through each product page to get the product information, if available. For simplicity, only the most important deatails are scraped, including the product's name, price, basic information, rating, and number of reviews. The information is formatted and saved into `ProductList.csv`

### `server.py`

This is where the magic happens. Using Langchain, the CSV data is loaded into the chatbot based on OpenAI's GPT 3.5-turbo model. The file also includes necessary functions to integrate with Slack, enabling localhost port 3000 to accept and reply to Slack requests, generating relevant output based on the data and the user's question. The bot can remember the last 5 messages sent and received *in the current server session*.

## Future Work and Improvements:

#### Web Scraping

- Scrape more comprehensive product data, and speed up the scraping if possible.
- Scan product pages to enumerate all possible XPaths or `class` names of features like price, reviews, etc. Some products have the details in different locations, and I may have missed some.

#### Server and Security

 - Create a permanent server to run the bot, instead of the temporary server for testing.
 - If used externally, put all sensitive data and keys into a `.env` file. 
 
#### Slack Bot

 - Optimize and tune the LLM for best results (e.g., adjust temperature), and test with different base models from OpenAI and others.
 - Optimize the way the product data is processed into the model by adjusting the size of the text splitting, etc.
 - Add support to process a multi-header CSV file into the model. Currently, I combine the data for each product into one line of text because that produced better results, which makes the CSV file not much different from a text file, ultimately. 
 - Add additional features for the bot in the workspace, such as enabling it to work in DMs, threads, etc.
 - Store product information in a database, and maintain a history of chat messages that persists longer than the temporary server's session. Currently, the data and memory are transient.

## Citations

I used the Langchain and Slack documentation for this project, in addition to adapting limited portions of code from [Stack Overflow](https://stackoverflow.com/questions/31276001/parse-xml-sitemap-with-python), [Github](https://github.com/Saurav-Shrivastav/Slackbot-tutorial), and [freeCodeCamp](https://www.freecodecamp.org/news/scraping-ecommerce-website-with-python/).
