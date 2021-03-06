var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var UserSchema = new Schema({
	email: String,
	credits: Number,
	uid: String,
	isAdmin: Boolean
});

module.exports = mongoose.model('User', UserSchema);
