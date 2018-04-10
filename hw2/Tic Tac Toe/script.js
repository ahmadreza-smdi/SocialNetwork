const BOARD_SIZE = 3,
EMPTY = "&nbsp;",
boxes = [];
var scores, moves, turn = 'X';

function init() {
createBoard();
startNewGame();
}

function createBoard() {
var board = document.createElement("table");
board.setAttribute("border", 1);
board.setAttribute("cellspacing", 0);

var cellId = 1;
for (var i = 0; i < BOARD_SIZE; i++) {
  var row = document.createElement("tr");
  board.appendChild(row);
  for (var j = 0; j < BOARD_SIZE; j++) {
    var cell = document.createElement("td");
    cell.setAttribute("height", 120);
    cell.setAttribute("width", 120);
    cell.setAttribute("align", "center");
    cell.setAttribute("valign", "center");
    cell.classList.add("col" + j, "row" + i);
    if (i === j) {
      cell.classList.add("ghotr0");
    }
    if (j === BOARD_SIZE - i - 1) {
      cell.classList.add("ghotr1");
    }
    cell.identifier = cellId;
    cell.addEventListener("click", onCellClicked);
    row.appendChild(cell);
    boxes.push(cell);
    cellId += cellId;
  }
}

document.getElementById("ttt").appendChild(board);
}

function startNewGame() {
scores = {
  X: 0,
  O: 0
};
moves = 0;
turn = "X";
boxes.forEach(function (box) {
  box.innerHTML = EMPTY;
});
}

function checkWining(clickedCell) {
// Get all cell classes
var memberOf = clickedCell.className.split(/\s+/);
for (var i = 0; i < memberOf.length; i++) {
  var testClass = "." + memberOf[i];
  var items = contains("#ttt " + testClass, turn);
  // winning condition: turn == BOARD_SIZE
  if (items.length === BOARD_SIZE) {
    return true;
  }
}
return false;
}

function contains(selector, text) {
var elements = document.querySelectorAll(selector);
return [].filter.call(elements, function (element) {
  return RegExp(text).test(element.textContent);
});
}

function onCellClicked() {
if (this.innerHTML !== EMPTY) {
  return;
}
this.innerHTML = turn;
moves += 1;
scores[turn] += this.identifier;
if (checkWining(this)) {
  alert("Winner: Player " + turn);
  startNewGame();
} else if (moves === BOARD_SIZE * BOARD_SIZE) {
  alert("Draw");
  startNewGame();
} else {
  turn = turn === "X" ? "O" : "X";
  document.getElementById("turn").textContent = "Player " + turn;
}
}

init();