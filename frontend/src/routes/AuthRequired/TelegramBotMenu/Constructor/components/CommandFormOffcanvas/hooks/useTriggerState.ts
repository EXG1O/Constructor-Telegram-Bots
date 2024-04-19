import { Dispatch, SetStateAction, useState } from 'react';

import { Data as BaseData } from '../components/Trigger';

type Data = BaseData | undefined;

function useTriggerState(initialData?: Data): [Data, Dispatch<SetStateAction<Data>>] {
	return useState<Data>(initialData);
}

export default useTriggerState;