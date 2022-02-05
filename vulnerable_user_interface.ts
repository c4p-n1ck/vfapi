import { Webview } from "https://deno.land/x/webview/mod.ts";

const webview = new Webview();

webview.navigate('http://localhost:8008/');
webview.run();
