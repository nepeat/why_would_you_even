<?php
// Composer
require __DIR__ . "/vendor/autoload.php";

// Connection
function create_redis() {
	$redis_host = getenv("REDIS_HOST") ?: "127.0.0.1";

	$redis = new Predis\Client(array(
		"scheme" => "tcp",
		"host" => $redis_host,
		"port" => 6379,
		"read_write_timeout" => "0"
	));

	return $redis;
}

$redis_data = create_redis();
$redis_pubsub = create_redis();


// Registration
$redis_data->hmset("bot:commands", array(
	"brainfuck" => "Evals brainfuck code.",
));

// Bot
function say($redis, $channel, $message) {
	$redis->publish("core:say", json_encode(array(
		"action" => "say",
		"channel" => $channel,
		"text" => $message
	)));
}

$pubsub = $redis_pubsub->pubSubLoop();
$pubsub->subscribe("command:brainfuck");

foreach ($pubsub as $message) {
	if ($message->kind !== "message" && $message->kind !== "pmessage") {
		continue;
	}

	$data = json_decode($message->payload);

	if (json_last_error() !== JSON_ERROR_NONE) {
		return;
	}

	$parts = explode(" ", $data->message->content, 2);
	$command = trim(str_replace("!", "", $parts[0]));
	$args = trim($parts[1]);

	switch ($command) {
		case "brainfuck":
			echo "Brainfucking " . $args;

			$result = igorw\brainfuck\execute($args);
			if (!empty($result)) {
				say($redis_data, $data->channel, $result);
			} else {
				say($redis_data, $data->channel, "Got no results from the eval.");
			}
	}
}
?>