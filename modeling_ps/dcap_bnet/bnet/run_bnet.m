

function [] = run_bnet(dataDirectory, resultDirectory)
success = true; %will be set to false if we catch an exception
warning off

try 
	%add codebase to path
	cd(dataDirectory);

	%load the parameters
	set_parameters()
	which 'run_general_bnet_experiment'

	[result, supports, allfold_result, case_idx] = run_general_bnet_experiment(parameters);
catch exc
	errorReport = getReport(exc,'extended');
	disp(errorReport);
	success = false;
end
cd(resultDirectory);

if success % store results
	
	save('result','result');
	save('parameters','parameters');
	save('pred','allfold_result');
	save('supports','supports');
	save('cases','case_idx');

else % store error Report and the parameters used so we can recreate
	save('errorReport','errorReport');
	
	if exist('parameters','var')
		save('parameters','parameters');
	end

end
	
exit;
