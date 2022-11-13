import {choc, on, fix_dialogs} from "https://rosuav.github.io/choc/factory.js";
const {BUTTON, DIALOG, FIGCAPTION, FIGURE, IMG, P, SECTION} = choc; //autoimport
ensure_popimg_dlg(); //Unnecessary overhead once Firefox 98+ is standard - can then be removed
fix_dialogs({close_selector: ".dialog_cancel,.dialog_close", click_outside: "formless"});

function ensure_popimg_dlg() {
	//Setting the z-index is necessary only on older Firefoxes that don't support true showModal()
	if (!DOM("#popimgdlg")) document.body.appendChild(DIALOG({id: "popimgdlg", style: "z-index: 999"}, SECTION([
		FIGURE([
			IMG({id: "popimg_img"}),
			FIGCAPTION(),
		]),
		P({style: "flex: 0; margin: 0"}, BUTTON({class: "dialog_close"}, "Close")),
	])));
}

//Add class=popup to links that should pop up
on("click", ".popup", e => {
	ensure_popimg_dlg();
	e.preventDefault();
	//An iframe can render an image, however, it won't claim the image's native
	//size as the iframe's size. In order to keep the size correct, it's easier
	//to have an actual img tag instead. TODO: Figure out a way to make images
	//zoomable by user, with a maximum size. This may entail burying them inside
	//an iframe themselves, in which case the logic goes in the inner page, and
	//this code here will just always use an iframe.
	const have = DOM("#popimg_img").tagName;
	const want = /\.htm[l]?$/.test(e.match.href) ? "IFRAME" : "IMG";
	if (have !== want) DOM("#popimg_img").replaceWith(choc(want, {id: "popimg_img"}));
	DOM("#popimg_img").src = ""; //Blank the popup first, to avoid weird displays esp stretching
	DOM("#popimg_img").src = e.match.href + (want === "IFRAME" ? "?inpopup" : "");
	let style = "";
	if (e.match.dataset.width) style += "width: " + e.match.dataset.width + "px;";
	if (e.match.dataset.height) style += "height: " + e.match.dataset.height + "px;";
	DOM("#popimg_img").style = style;
	set_content("#popimgdlg figcaption", e.match.title || "");
	DOM("#popimgdlg").showModal();
});

//When loaded inside an iframe, hide the copyright/license - it'll be clear from the
//outer page.
if (location.search === "?inpopup") document.body.classList.add("inpopup");
