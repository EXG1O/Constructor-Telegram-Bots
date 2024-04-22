import { Dispatch, SetStateAction, useState } from 'react';

import { Data as BaseData } from '../components/TriggerBlock';

type Data = BaseData | undefined;

function useTriggerState(initialData?: Data): [Data, Dispatch<SetStateAction<Data>>] {
	return useState<Data>(initialData);
}

export default useTriggerState;