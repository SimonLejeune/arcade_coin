var config = require('./config.json');
var mongoose = require('mongoose');
var connectString = 'mongodb://' + config.dbUser + ':' + config.dbPassword + '@ds147974.mlab.com:47974/arcade_borne'
var User = require('./models/user.js');

mongoose.connect(connectString, {useNewUrlParser: true});


console.log('Starting coin add...');
User.find({}, function (err, doc) {
	if (doc) {
		for(var i = 0; i < doc.length; i++) {
			doc[i].credits++;
			if (i === doc.length - 1) {
				doc[i].save().then(function () {
					mongoose.disconnect();
					console.log('Job done! Mongoose killed');
				});
			} else {
				doc[i].save();
			}
		}

	}
});
