import { useContext } from 'react';

import VariablesContext, { VariablesContextProps } from '../contexts/VariablesContext';

function useVariables(): VariablesContextProps {
	const variablesContext = useContext<VariablesContextProps | undefined>(VariablesContext);

	if (variablesContext === undefined) {
		throw new Error('useVariables must be used with a VariablesContext!');
	}

	return variablesContext;
}

export default useVariables;