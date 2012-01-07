import datediff

def whom(state, now, when) :
	whom = list()
	for who in state :
		if 'e' not in state[who] or 's' not in state[who] :
			continue

		if when <= state[who]['e'] and state[who]['s'] <= when :
			whom.append(who)
	whom.sort()

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
		verbal = 'is'
	else :
		temporal = 'in %s' % datediff.differ(when - now)
		verbal = 'will be'

	return '%s %s here %s.' % (whom, verbal, temporal)

"""
jim is here now
jim and rhys will be here in 23 minutes.
nobody is here now
"""
