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
$commands = array(
	"brainfuck" => "Evals brainfuck code.",
	"encrypt" => "Encrypts your strings!"
);

$redis_data->hmset("bot:commands", $commands);

// Bot
function say($redis, $channel, $message) {
	$redis->publish("core:say", json_encode(array(
		"channel" => $channel,
		"text" => $message
	)));
}

$pubsub = $redis_pubsub->pubSubLoop();

function make_channel($x) { return "command:" . $x; }
$pubsub->subscribe(array_map('make_channel', array_keys($commands)));

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

			$result = "```" . shell_exec("php safe_brainfuck.php " . escapeshellarg($args) . " 2>&1; echo $?") . "```";

			say($redis_data, $data->channel, $result);
			break;
		case "encrypt":
			$result = sprintf("<@%s>
**MD5** - %s
**SHA1** - %s
**SHA256** - %s",
				$data->author->id,
				md5($args),
				hash("sha1", $args),
				hash("sha256", $args)
			);

			say($redis_data, $data->channel, $result);
			break;
	}
}
?>
