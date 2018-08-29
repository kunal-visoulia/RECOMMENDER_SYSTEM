import numpy as np
from fetch_lastfm import fetch_lastfm
from lightfm import LightFM

min_plays=200
data,dic,res=fetch_lastfm(min_plays)

model = LightFM(loss='warp')
model.fit(data['matrix'], epochs=30, num_threads=2)


def get_recommendations(model,coo_mtrx,users_ids):
    n_items=coo_mtrx.shape[1]
	
    for user in users_ids:
	#known positives
	user_sha_id=res[int(user)]

	i=1
	top_3_artists=[]
	list_of_liked_artists=dic[user_sha_id]
	while i<4:
		top_3_artists.append(list_of_liked_artists[i][0])
		i+=1

	print 'Artists liked by user %s:' % user
	for x in top_3_artists:
		print '   - %s' % x
   	
		

	# Artists the model predicts they will like
       	scores = model.predict(user, np.arange(n_items))
        top_scores = np.argsort(-scores)[:3]
	print '\n'
        print 'Recomendations for user %s:' % user
        
       	for x in top_scores.tolist():
             for artist, values in data['artists'].iteritems():
             	if int(x) == values['id']:
                    print '   - %s' % values['name']

        print '\n' 

us=data['users']-3
user_1 = raw_input('Select user_1 (0 to %s): ' % us)
user_2 = raw_input('Select user_2 (0 to %s): ' % us)
user_3 = raw_input('Select user_3 (0 to %s): ' % us)
print '\n' 

get_recommendations(model, data['matrix'], [user_1, user_2, user_3])


