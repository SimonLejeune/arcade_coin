var cron = require('node-cron');
const spawn = require("child_process").spawn;
const addCoin =  function () {
        spawn('node',["coinAdd.js"]);
}


 
cron.schedule('*/20 * * * * *', () => {
	addCoin();
	console.log('done');
});
