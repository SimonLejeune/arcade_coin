/**
 * Created by julien on 17/04/17.
 */

var request = require('request');
var sleep = require('sleep-sync');
var { NFC } = require('nfc-pcsc');
var S = require('string');
var mongoose = require('mongoose');
var User = require('./models/user.js');
var config = require('./config.json');
var Gpio = require('onoff').Gpio; //include onoff to interact with the GPIO
var coin = new Gpio(21, 'out'); //use GPIO pin 4, and specify that it is output

var connectString = 'mongodb://' + config.dbUser + ':' + config.dbPassword + '@ds147974.mlab.com:47974/arcade_borne'

mongoose.connect(connectString, {useNewUrlParser: true});

const nfc = new NFC(); const apiUrl = 'https://whatsupdoc.epitech.eu/card/';

let lTrigger = Date.now();

const spawn = require("child_process").spawn;
const keySend =  function () {
	spawn('python',["keyboard.py"]);
}

nfc.on('reader', reader => {
    console.log(`${reader.reader.name} device attached`);
    reader.on('card', card => {
        if (card.type === 'TAG_ISO_14443_3') {
            if (Date.now() - lTrigger >= 1000) {
                lTrigger = Date.now();
                let login = "";
                let uid = S(card.uid).toUpperCase().s;
                lTrigger = Date.now();
                console.log(uid);
		request.get({ url: '' + apiUrl + uid, timeout: 5000 }, function (err, res, body) {
                            if (err === null) {
				login = JSON.parse(body);
				if (login.login) {
					User.findOne({email: login.login}, function (err, doc) {
						if (doc) {
							if (doc.uid != uid)
								doc.uid = uid;
							if (doc.isAdmin === true) {
								pushButton();
							} else if (doc.credits > 0) {
								doc.credits = doc.credits - 1;
								pushButton();
							}
							doc.save();
						} else {
							var userObj = new User({
								email: login.login,
								uid: uid,
								credits: 4,
								isAdmin: false
							});
							userObj.save();
							pushButton();
						}
					});
				}
			    }
		});
            }
        }
    });

    reader.on('error', err => {
        console.log(`An error occured with the reader: ${err}`);
    });
});

function pushButton() { //function to start blinking
	console.log("PUSH BUTTON")
  coin.writeSync(1); //set pin state to 1 (turn LED on)
	sleep(250);
  coin.writeSync(0); //set pin state to 0 (turn LED off)
}

nfc.on('error', err => {
    console.log(`Error occurred: ${err}`);
});

process.on('SIGINT', () => {
    console.log('Exiting program...');
    process.exit(0);
});
