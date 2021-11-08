const AWS = require('aws-sdk');
const mqtt = require("mqtt");

/* 
This code uses callbacks to handle asynchronous function responses.
It currently demonstrates using an async-await pattern. 
AWS supports both the async-await and promises patterns.
For more information, see the following: 
https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function
https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises
https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/calling-services-asynchronously.html
https://docs.aws.amazon.com/lambda/latest/dg/nodejs-prog-model-handler.html 
*/
exports.main = async function (event, context) {

    const client = mqtt.connect("mqtt://broker.hivemq.com", 1883);

    const connectedPromise = new Promise((resolve, reject) => {
        client.on('connect', () => {
            resolve()
        })
    })

    await connectedPromise


    try {
        var method = event.httpMethod;
        // Get name, if present
        var widgetName = event.path.startsWith('/') ? event.path.substring(1) : event.path;

        if (method === "GET") {
            // GET / to get the names of all widgets
            return {
                statusCode: 200,
                headers: {},
                body: JSON.stringify({ result: 'ok' })
            };
        } else if (method === "POST") {
            console.log(JSON.parse(event.body))
            await client.publish("ttm4160/carcontrols", JSON.stringify(JSON.parse(event.body)))
            return {
                statusCode: 200,
                headers: {
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                },
                body: JSON.stringify({ result: "ok" })
            }

        }
    } catch (error) {
        var body = error.stack || JSON.stringify(error, null, 2);
        return {
            statusCode: 400,
            headers: {},
            body: body
        }
    }
}