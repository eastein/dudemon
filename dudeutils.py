import datediff

"""
jim is here now
jim and rhys will be here in 23 minutes.
nobody is here now
"""
def whom(state, now, when) :
	whom = list()
	for who in state :
		if 'e' not in state[who] or 's' not in state[who] :
			continue

		if when <= state[who]['e'] and state[who]['s'] <= when :
			whom.append(who)
	whom.sort()
	plural = len(whom) > 1

	if len(whom) > 2 :
		whom = ', '.join(whom[:-1]) + ', and ' + whom[-1]
	elif len(whom) == 2 :
		whom = '%s and %s' % (whom[0], whom[1])
	elif len(whom) == 0 :
		whom = 'nobody'
	else :
		whom = whom[0]

	if now == when :
		temporal = 'now'
		if plural :
			verbal = 'are'
		else :
			verbal = 'is'
	else :
		temporal = 'in %s' % datediff.differ(when - now)
		verbal = 'will be'

	return '%s %s here %s.' % (whom, verbal, temporal)

def overlap(state, s, e) :
	whom = list()
	for who in state :
		if 'e' not in state[who] or 's' not in state[who] :
			continue

		w_s = state[who]['s']
		w_e = state[who]['e']

		if s < w_s and e > w_e :
			whom.append(who)
			continue
		elif s >= w_s and s <= w_e :
			whom.append(who)
			continue
		elif e >= w_s and e <= w_e :
			whom.append(who)
			continue

	whom.sort()
	return whom

def oxford(l) :
	l = l[:]
	if not l :
		raise RuntimeError
	if len(l) > 2 :
		l[len(l)-1] = 'and %s' % l[len(l)-1]
		return ', '.join(l)
	elif len(l) == 2 :
		return '%s and %s' % (l[0], l[1])
	else :
		return l[0]
