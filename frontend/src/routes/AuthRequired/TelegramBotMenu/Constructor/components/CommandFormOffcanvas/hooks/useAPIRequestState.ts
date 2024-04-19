import { Dispatch, SetStateAction, useState } from 'react';

import { Data as BaseData } from '../../APIRequest';

type Data = BaseData | undefined;

function useAPIRequestState(initialData?: Data): [Data, Dispatch<SetStateAction<Data>>] {
	return useState<Data>(initialData);
}

export default useAPIRequestState;