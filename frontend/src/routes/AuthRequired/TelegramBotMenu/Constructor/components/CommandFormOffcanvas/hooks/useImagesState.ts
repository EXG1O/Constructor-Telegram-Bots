import { Dispatch, SetStateAction, useState } from 'react';

import { Data as BaseData } from '../components/Images';

type Data = BaseData | undefined;

function useImagesState(initialData?: Data): [Data, Dispatch<SetStateAction<Data>>] {
	return useState<Data>(initialData);
}

export default useImagesState;