var util = require("util");
var redis = require("redis");

var redis_host = process.env.REDIS_HOST || "127.0.0.1";
var redis_port = process.env.REDIS_PORT || 6379;

var client = redis.createClient(redis_port, redis_host);
var pubsub = redis.createClient(redis_port, redis_host);

function say(channel, text) {
	client.publish("core:say", JSON.stringify({
		channel: channel,
		"text": text
	}));
}

function redis_error(err) {
	console.log("[RedisError] " + err);
}

client.on("error", redis_error);
pubsub.on("error", redis_error);

pubsub.on("message", function (channel, message) {
	try {
		var data = JSON.parse(message);
	} catch (e) {
		return;
	}

	console.log("Parsed data %s", message);

	var results = "";

	var parts = data.message.content.split(" ");
	var command = parts[0].replace("!", "").trim();
	var args = parts.slice(1).join(" ");

	console.log("DEBUG: %s || %s || %s", parts, command, args);

	switch (command) {
		/* Zephy - Today at 1:54 AM
			wut
			all of them
			pyval, pyxec, jsval :D
		*/

		// "jsval" - Done.
		case "node_eval":
			console.log("Doing an eval on '%s'", args);
			try {
				results = eval(args);
			} catch (e) {
				results = e;
			}

			break;
		case "game":
			client.publish("core:game", JSON.stringify({
				game: args
			}));
			results = "Game set to " + args;
			break;
	}

	if (results && results !== "") {
		try {
			say(data.channel, results);
		} catch (e) {
			say(data.channel, util.format("An exception happened.\n```%s```", e));
		}
	}
});

function init_pubsub() {
	pubsub.subscribe("command:node_eval");
}

client.hmset("bot:commands", [
	"node_eval", "It does an eval on the node container. The pain begins here.",
	"game", "Sets the bot game status."
], function(err, _reply) {
	console.log("Registered in commands dict!");

	client.publish("core:reload", "");

	init_pubsub();
});
