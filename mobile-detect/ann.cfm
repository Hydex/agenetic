<cfsetting showdebugoutput="false">
<cfset strings = StructNew()>

<cffile action="read" file="#GetDirectoryFromPath(GetCurrentTemplatePath())#/agents.txt" variable="agents">

<!--- create a list of all tokens found in an agent string --->
<cfloop list="#agents#" delimiters="#chr(13)#" index="agent">
	<cfset tokens = tokenise(agent)>
	<cfloop array="#tokens#" index="token">
		<cfif NOT StructKeyExists(strings, token)>
			<cfset strings[token] = 0>
		</cfif>
		<cfset strings[token] += 1>
	</cfloop>
</cfloop>

<!--- get an array of words so that we have ids for each --->
<cfset inputValues = StructKeyArray(strings)>
<cfset index = 0>
<cfloop array="#inputValues#" index="val">
	<cfset index += 1>
	<cfif strings[val] EQ 1>
		<cfset StructDelete(strings, val)>
	</cfif>
</cfloop>
<cfset inputValues = StructKeyArray(strings)>

<!--- setup the output values --->
<cfset outputValues = ["desktop","robot","mobile","tablet"]>
<cfdump var="#outputValues#">

<cfset inputSize = ArrayLen(inputValues)>
<cfset hiddenSize = 10>
<cfset outputSize = ArrayLen(outputValues)>

<cfset ga = CreateObject("component", "ga")>
<cfset g = ga.seedGA(1, inputSize, hiddenSize, outputSize)>
<cfset pop = ga.getPopulation()>

<cfset M = CreateObject("component", "Matrix")>

<!--- figure out the fitness for each populate --->
<cfset annCount = 0>
<cfloop array="#pop#" index="ann">
	<cfset annCount += 1>
	<cfset score = 0>

	<cfoutput><h1>#annCount#</h1></cfoutput>

	<!--- run each ANN and get the result --->
	<cfloop list="#agents#" delimiters="#chr(13)#" index="agent">
		<cfset userAgent = GetToken(agent, 1, ",")>
		<cfset answer = Replace(GetToken(agent, 2, ","), """", "", "ALL")>
		<cfset correct = ArrayFind(outputValues, answer)>
		
		<cfif correct GTE 1>
			<cfset tokens = tokenise(userAgent)>
			
			<!--- assemble the input vector --->
			<cfset inputVector = CreateObject("component", "Matrix")>
			<cfset inputVector.setWidth(1).setHeight(inputSize).init()>
			
			<!--- <cfset Arrayset(inputVector, 1, inputSize, 0)> --->
			<cfloop array="#tokens#" index="t">
				<cfif StructKeyExists(strings, t)>
					<cfset inputVector.setElem(ArrayFind(inputValues, t), 1, 1)>
				</cfif>
			</cfloop>
			
			<!--- run the weights --->
			<cfset acc1 = M.multiply(inputVector, ann.first_weights).divide(inputSize)>
			<cfset acc2 = Threshold(acc1, ann.first_thresholds)>
			<cfset acc3 = M.multiply(acc2, ann.second_weights)>
			<cfset acc4 = Threshold(acc3, ann.second_thresholds)>
			
			<!--- evaluate the 'fitness' for the output.
			we'll use:
				1	for a right bit
				0	for a wrong bit
			--->
			<cfloop from="1" to="#arrayLen(acc4)#" index="ic">
				<cfif acc4[ic] EQ 1 AND ic EQ correct>
					<cfset score += 1>
				<cfelseif acc4[ic] EQ 0 AND ic NEQ correct>
					<cfset score += 1>
				</cfif>
			</cfloop>
			
			<cfoutput><table>
				<tr>
					<td>#acc4.render()#</td>
					<td>=</td>
					<td>#ann.second_thresholds.render("blue")#</td>
					<td>#ann.second_weights.render()#</td>
					<td>#ann.first_thresholds.render("blue")#</td>
					<td>#acc1.render("red")#</td>
					<td>#ann.first_weights.render()#</td>
					<td>#inputVector.render()#</td>
				</tr>
			</table><h2>#score#</h2></cfoutput>
		
		<cfelse>
			<cfthrow message="answer #answer# not found in output variables. Ensure the training data is correct">
		</cfif>

	</cfloop>
	
	<cfoutput>#score#</cfoutput>
	<cfabort>
</cfloop>





<cffunction name="tokenise">
	<cfargument name="agent" type="string">
	<cfset agent = LCase(agent)>
	<cfset agent = REReplace(agent, "[^A-Za-z1-9.]", " ", "all")>
	<cfreturn ListToArray(agent, " ", false)>
</cffunction>
<cffunction name="threshold">
	<cfargument name="input">
	<cfargument name="thresholds">
	
	<cfset var res = CreateObject("component", "Matrix")>
	
	<cfif input.width() NEQ 1 or thresholds.width() NEQ 1>
		<cfthrow message="input and thresholds must only be 1 column wide">
	</cfif>
	
	<cfset res.setWidth(1).setHeight(input.height()).init()>
	
	<cfloop from="1" to="#input.height()#" index="h">
		<cfif input.getElem(h, 1) GT thresholds.getElem(h, 1)>
			<cfset res.setElem(h, 1, 1)>
		</cfif>
	</cfloop>
	
	<cfreturn res>
</cffunction>