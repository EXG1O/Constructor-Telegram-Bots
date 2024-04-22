import { Dispatch, SetStateAction, useState } from 'react';

import { Value, defaultValue } from '../components/MessageBlock';

function useMessageState(initialValue: Value = defaultValue): [Value, Dispatch<SetStateAction<Value>>] {
	return useState<Value>(initialValue);
}

export default useMessageState;