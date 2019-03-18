/*
 * This is a JavaScript Scratchpad.
 *
 * Enter some JavaScript, then Right Click or choose from the Execute Menu:
 * 1. Run to evaluate the selected text (Ctrl+R),
 * 2. Inspect to bring up an Object Inspector on the result (Ctrl+I), or,
 * 3. Display to insert the result in a comment after the selection. (Ctrl+L)
 */

function test() {
	var tbody = $('#products > tbody');
	var result = [];
	tbody.find('.orders').each(function(index, tr) {
		$(tr.children[1]).find('tr').each(function(i, row) {
			var name = row.children[0].textContent.trim();
			var link = row.children[1].children[0].href;
			result.push([name, link]);
		});
	});
	return result;
}

test().toString();

