def strDiff(str1, str2):
	res = ""
	for i in range(len(str2)):
		if res + str2[i] == str1[:i + 1]:
			res += str2[i]
		else:
			res = res[:-1]
	return len(res) * 100 / len(str1)