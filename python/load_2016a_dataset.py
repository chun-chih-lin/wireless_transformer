import _pickle as pickle


def main():
	data_loc = "C:\\Users\\chunchi.CAMPUS\\Downloads\\RML2016.10a.tar\\RML2016.10a\\RML2016.10a_dict.pkl"
	with open(data_loc, 'rb') as f:
		data = pickle.load(f, encoding='latin1')

	print(type(data), len(data))
	keys = data.keys()
	for key in keys:
		print(f"{key = }, {type(key) = }")
		value = data.get(key)
		print(f"{type(value) = }, {len(value) = }, {value.shape = }")
		
		value_e = value[0, :, :]
		print(f"{value_e = }")
		break

	print(f"{keys = }")
	pass

if __name__ == '__main__':
	main()