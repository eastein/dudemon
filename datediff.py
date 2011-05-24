class Bad(Exception) :
	pass

def plur(v, s) :
	if v > 0 :
		if v == 1 :
			return '1 %s' % s
		else :
			return '%d %ss' % (v, s)

def differ(sec, detail=2) :
	M = 60
	H = 60
	D = 24
	Y = 365
	scord = ['second', 'minute', 'hour', 'day']
	scales = {
		'day' : Y,
		'hour' : D,
		'minute' : H,
		'second' : M
	}
	chunks = []
	for k in scord :
		v = sec % scales[k]
		sec -= v
		sec /= scales[k]
		c = plur(v, k)
		if c :
			chunks.append(c)
	if sec > 0 :
		chunks.append(plur(sec, 'year'))

	relev = chunks[-detail:]
	relev.reverse()
	if not relev :
		return 'a jiffy'
	return ', '.join(relev)

def dur2sec(s) :
	r = 0
	try :
		fields = s.split(':')
		if len(fields) == 1 and len(s) > 2 :
			fields = [s[:-2], s[-2:]]
		nums = map(lambda s: int(s), fields)
		if len(nums) not in [1,2] :
			raise Bad
		if len(nums) == 1 :
			r = 60 * nums[0]
		if len(nums) == 2 :
			r = 3600 * nums[0] + 60 * nums[1]
	except :
		raise Bad
	if r < 0 :
		raise Bad
	return r
