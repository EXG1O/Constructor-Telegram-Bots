import { Dispatch, SetStateAction, useState } from 'react';

import { Value, defaultValue } from '../components/Message';

function useMessageState(initialValue: Value = defaultValue): [Value, Dispatch<SetStateAction<Value>>] {
	return useState<Value>(initialValue);
}

export default useMessageState;