<?php
header("Content-Type: application/json; charset=UTF-8");

$Cached = null;

function BuildRESTURL($Settings = null) : string
{
	if (is_null($Settings))
	{
		$Settings = $GLOBALS['DefaultSettings'];
	}

	$url_base = "https://circleci.com/api/v1.1/project/:vcs-type/:username/:project/latest/artifacts?branch=:branch&filter=:filter";

	$url = str_replace(array_keys($Settings), $Settings, $url_base);

	return $url;
}

function GetAgent($fallback = "PSO2es Tweaker 1.1") : string
{
	if ($_SERVER)
	{
		if (array_key_exists("HTTP_USER_AGENT", $_SERVER))
		{
			return $_SERVER['HTTP_USER_AGENT'];
		}
	}
	return $fallback;
}

function GetRESTData($url, $retry = 3) : string
{
	if ($retry == -1)
	{
		error_log("Could not download REST data");
		return "";
	}

	$httpopts = array(
	  'http'=>array(
		'method'=>"GET",
		'user_agent'=>GetAgent(),
//------------------------------------------------------------------------------
		'header'=>"Accept: application/json\r\n"
	  )
	);

	$httpheader = stream_context_create($httpopts);
	$contents = null;

	try
	{
		$contents = @file_get_contents($url, false, $httpheader);

		if ($contents === false)
		{ // Handle exception and retry
			return GetRESTData($url, ($retry - 1));
		}
	}
	catch (Exception $e)
	{ // Handle exception
		error_log($e);
		return "";
	}

	if (is_null($contents))
	{
		error_log("file_get_contents() is disabled");
		return "";
	}

	return $contents;
}

function GetRESTArray($Settings = null) : array
{
	if (is_null($Settings))
	{
		$Settings = $GLOBALS['DefaultSettings'];
	}

	$url = BuildRESTURL($Settings);

	$content = GetRESTData($url);

	if ($content == "")
	{
		return [];
	}

	$Data = json_decode($content, TRUE);

	if (is_null($Data))
	{
		error_log(json_list_error_msg());
		//json_last_error
		return [];

	}

	return $Data;
}

function GetPatchArray($Settings = null, $path = "patchBeta.zip"): array
{
	if (is_null($Settings))
	{
		$Settings = $GLOBALS['DefaultSettings'];
	}

	global $Cached;
	if (is_null($Cached))
	{
		$Data = GetRESTArray($Settings);
		$Cached = $Data;
	}
	else
	{
		$Data = $Cached;
	}

	if ($Data == [])
	{
		error_log("Can not fetch JSON");
		return [];
	}

	$paths = array_column($Data, 'path');

	if ($paths == [])
	{
		error_log("There no paths in JSON");
		return [];
	}

	$key = array_keys($paths, $path);

	if (!$key)
	{
		error_log("Can not find a good path in JSON");
		return [];
	}
	return $Data[$key[0]];
}

function GetPatchURL($Settings = null, $path = "patchBeta.zip"):  string
{
	if (is_null($Settings))
	{
		$Settings = $GLOBALS['DefaultSettings'];
	}

	$Data = GetPatchArray($Settings, $path);

	if ($Data == [])
	{
		return "";
	}

	if (array_key_exists("url", $Data))
	{
		return $Data["url"];
	}

	error_log("No url in JSON entry");

	return "";
}

function GetPatchVersion($Settings = null, $path = "patchBeta.txt", $retry = 3) : string
{
	if (is_null($Settings))
	{
		$Settings = $GLOBALS['DefaultSettings'];
	}

	$url = GetPatchURL($Settings, $path);

	if ($retry == -1)
	{
		error_log("Could not download version file");
		return "";
	}

	if ($url == "")
	{
		return "Unknown";
	}

	$contents = "";
	try
	{
		$contents = @file_get_contents($url);
		if ($contents === false)
		{ // Handle the error and retry
			return GetPatchVersion($Settings, $path, ($retry - 1));
		}
	}
	catch (Exception $e)
	{ // Handle exception
		error_log($e);
		error_log("Can not download version file");
		return "";
	}

	if (is_null($contents))
	{
		error_log("file_get_contents() is disabled");
		return "";
	}

	if ($contents == "")
	{
		error_log("Fetch empty version file");
		return "NULL";
	}

	return rtrim($contents);
}

function MakePatchFeed($Settings = null) : string
{
	if (is_null($Settings))
	{
		$Settings = $GLOBALS['DefaultSettings'];
	}

	$Feed = $GLOBALS['DefaultFeed'];
	$version = GetPatchVersion($Settings);
	$url = GetPatchURL($Settings);
	$compatible = ($version != '' && $url != '');
	$message = str_replace(array_keys($Settings), $Settings, $Feed["patch_message"]);

	$Feed["patch_version"] = $version;
	$Feed["patch_url"] = $url;
	$Feed["patch_compatible"] = $compatible;
	$Feed["patch_message"] = $message;

	$Data = json_encode($Feed, JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES);

	return $Data;
}

function CheckPOSTSettings($CGI = null) : array
{
	$Settings = $GLOBALS['DefaultSettings'];

	if (!is_null($CGI) and $CGI)
	{
		if (array_key_exists("username", $CGI))
		{
			$Settings[":username"] = $CGI["username"];
		}

		if (array_key_exists("branch", $CGI))
		{
			$Settings[":branch"] = $CGI["branch"];
		}

		if (array_key_exists("project", $CGI))
		{
			$Settings[":project"] = $CGI["project"];
		}
	}

	return $Settings;
}

$DefaultSettings = Array
(
	":vcs-type" => "github",
	":username" => "PolCPP",
	":project"=> "PSO2es-Translation",
	":branch" => "master",
	":filter" => "successful",
);

$DefaultFeed = Array
(
	"patch_version" => "000",
	"patch_url" => "https://XX-XXXXXXXX-gh.circle-artifacts.com/0/patchBeta.zip",
	"patch_compatible" => 1,
	"patch_message" => "CircleCI: :username/:project/:branch build",
);

function main()
{
	$Settings = CheckPOSTSettings($_GET);
	print(MakePatchFeed($Settings));
}

main();
?>
