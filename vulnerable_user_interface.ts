import { Webview } from "https://deno.land/x/webview/mod.ts";

const webview = new Webview(
	title: "Vulnerable User Interface"
);

webview.navigate('http://localhost:8008/');
webview.run();
