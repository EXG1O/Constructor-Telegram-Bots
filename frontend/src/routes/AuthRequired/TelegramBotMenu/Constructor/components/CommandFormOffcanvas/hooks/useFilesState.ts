import { Dispatch, SetStateAction, useState } from 'react';

import { Data as BaseData } from '../components/Files';

type Data = BaseData | undefined;

function useFilesState(initialData?: Data): [Data, Dispatch<SetStateAction<Data>>] {
	return useState<Data>(initialData);
}

export default useFilesState;