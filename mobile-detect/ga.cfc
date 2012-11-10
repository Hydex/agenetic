component {

	variables.population = ArrayNew(1);

	public void function seedGA(required numeric size, 
			required numeric inSize, 
			required numeric hiddenSize, 
			required numeric outSize)
	{
		variables.inSize = inSize;
		variables.hiddenSize = hiddenSize;
		variables.outSize = outSize;
		
		for (i = 1; i lte size; i++) {
			matrices = StructNew();
			matrices.first_weights = getWeights(inSize, hiddenSize);
			matrices.first_thresholds = getThresholds(hiddenSize);
			matrices.second_weights = getWeights(hiddenSize, outSize);
			matrices.second_thresholds = getThresholds(outSize);
			ArrayAppend(variables.population, matrices);
		}
	}
	
	public Matrix function getWeights(required numeric width, required numeric height) {
		var m = CreateObject("component", "Matrix");
		m.setWidth(width);
		m.setHeight(height);
		m.randomFill(0, 1);
		return m;
	}

	public Matrix function getThresholds(required numeric height) {
		var m = CreateObject("component", "Matrix");
		m.setHeight(height);
		m.randomFill(0, 2);
		return m;
	}
	
	public Array function getPopulation() {
		return variables.population;
	}

}