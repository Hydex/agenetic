component {

	variables.width = 1;
	variables.height = 1;
	variables.values = ArrayNew(1);

	public Matrix function setWidth(required numeric width) {
		if (width GTE 1) {
			variables.width = Int(width);
		} else {
			throw("Unable to set the width of a matrix to 0 or less")
		}
		return this;
	}

	public Matrix function setHeight(required numeric height) {
		if (height GTE 1) {
			variables.height = Int(height);
		} else {
			throw("Unable to set the height of a matrix to 0 or less")
		}
		return this;
	}
	
	public numeric function width() { return variables.width; }
	public numeric function height() { return variables.height; }

	public Matrix function init(numeric fillValue = 0) {
		for (i=1; i lte variables.height; i++) {
			var row = ArrayNew(1);
			ArraySet(row, 1, variables.width, fillValue);
			//for (j=1; j lt variables.width; j++) {
			//	ArrayAppend(row, fillValue);
			//}
			ArrayAppend(variables.values, row);
		}
		return this;
	}

	public Matrix function randomFill(required numeric min, required numeric max) {
		var lmin = min * 1000;
		var lmax = max * 1000;
		for (i=1; i lte variables.height; i++) {
			var row = ArrayNew(1);
			for (j=1; j lte variables.width; j++) {
				ArrayAppend(row, randRange(lmin, lmax, "SHA1PRNG")/1000);
			}
			ArrayAppend(variables.values, row);
		}
		return this;
	}
	
	public numeric function getElem(required numeric row, required numeric col) {
		return variables.values[row][col];
	}
	public Matrix function setElem(required numeric row, required numeric col, required numeric value) {
		variables.values[row][col] = value;
		return this;
	}
	
	public Matrix function multiply(required Matrix two, required Matrix one) {
		var acc = 0;
		var res = CreateObject("component", "Matrix");
		if (one.width() NEQ two.height()) {
			throw("Matrices must have compatible sizes");
		}
		// initialise the result
		res.setWidth(two.width()).setHeight(one.height()).init();
		
		for (i=1; i lte one.height(); i++) { // loop over left hand rows
			for (j=1; j lte two.width(); j++) { // loop over the right hand columns
				acc = 0;
				for (k=1; k lte one.width(); k++) { // loop over each element pair and sum multiplicands
					acc += (one.getElem(i, k) * two.getElem(k, j));
				}
				res.setElem(i, j, acc);
			}
		}
		return res;
	}
	
	public Matrix function divide(required numeric divisor) {
		for (i=1; i lte variables.height; i++) {
			for (j=1; j lte variables.width; j++) {
				setElem(i, j, getElem(i, j) / divisor);
			}
		}
		return this;
	}
	
	public String function render(string color = "black") {
		var out = "<table>";
		for (i=1; i lte variables.height; i++) {
			out &= "<tr>";
			for (j=1; j lte variables.width; j++) {
				out &= "<td";
				style = "color: #color#";
				if (j EQ 1) { style &= ";border-left: 1px solid black"; }
				if (j EQ variables.width) { style &= ";border-right: 1px solid black"; }
				out &= " style='#style#'>#getElem(i, j)#</td>";
			}
			out &= "</tr>";
		}
		out &= "</table>";
		return out;
	}
}