import {on, fix_dialogs} from "https://rosuav.github.io/choc/factory.js";
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
	DOM("#popimg_img").src = e.match.href;
	set_content("#popimgdlg figcaption", e.match.title || "");
	DOM("#popimgdlg").showModal();
});
