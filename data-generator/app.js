const UserAgent = require("user-agents"); // https://github.com/intoli/user-agents
const createCsvWriter = require('csv-writer').createObjectCsvWriter; // https://stackabuse.com/reading-and-writing-csv-files-with-node-js/

AMOUNT_OF_USER_AGENTS =1 *100000

data = new Map();

console.log("Starting...");
console.log("Generating user agents...");

const userAgent = new UserAgent({ deviceCategory: 'desktop' });
const userAgents = Array(AMOUNT_OF_USER_AGENTS).fill().map(() => userAgent());

console.log("Counting user agents...");

for (let singleUA of userAgents)
{
    string = singleUA.toString()
    if (!data.has(string))
    {
        data.set(string,1);
    } else 
    {
        data.set(string,data.get(string)+1);
    }
}

console.log("Saving to CSV...");

const csvWriter = createCsvWriter({
    path: 'user-agents-strings-with-counts.csv',
    header: [
        {id: 'string', title: 'User Agent String'},
        {id: 'count', title: 'Count'},
    ]
});

csvWriter
    .writeRecords([...data].map(([k,v]) => { return {string: k, count: v}}))
    .then(()=> console.log('The CSV file was written successfully'));
