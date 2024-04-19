import { Dispatch, SetStateAction, useState } from 'react';

import { Value as BaseValue } from '../components/DatabaseRecord';

type Value = BaseValue | undefined;

function useDatabaseRecordState(initialValue?: Value): [Value, Dispatch<SetStateAction<Value>>] {
	return useState<Value>(initialValue);
}

export default useDatabaseRecordState;