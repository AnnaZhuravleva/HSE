package ndarray

import "errors"

type NDArray struct {
	shape []uint32
}

func New(shape ...uint32) *NDArray {
	ndarr := new(NDArray)
	ndarr.shape = shape

	return ndarr
}

func (nda *NDArray) Idx(indicies ...uint32) (uint32, error) {
	var i, num uint32 = 1, 0
	if len(indicies) == len(nda.shape) {
		for li := len(indicies) - 1; li >= 0; li-- {
			if indicies[li] < nda.shape[li] {
				num += indicies[li] * i
				i *= nda.shape[li]
			} else {
				return 0, errors.New("error")
			}
		}
		return num, nil
	}
	return 0, errors.New("error")
}
