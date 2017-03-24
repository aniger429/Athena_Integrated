from flask import request, redirect, url_for
from controllers.Candidate_Analysis.Candidate_Identification_Final import *
from DBModels.Tweet import *
from DBModels.MongoDB_Manager import *

def new_analysis():
    flevel = request.form['first-level']
    slevel = request.form['second-level']
    tlevel = request.form['third-level']
    candidate_name = request.form['candidate-name']
    use_workspace = request.form['use-workspace-name']
    new_workspace = request.form['new-workspace-name']


    if use_workspace == "create":
        create_new_workspace(new_workspace)
        use_workspace = new_workspace

    db = get_db_instance(use_workspace)

    # first level
    if flevel == "candidate":
        print("flevel: candidate")
        tweets = get_everything()
        populate_new_workspace(tweets)
        # print (tweets)
        candidate_presence = identify_candidate(tweets)
        into_new_db(tweets, candidate_presence,db)

        if slevel == "none":
            print("slevel: none")
        elif slevel == "topic":
            print("slevel: topic")

            if tlevel == "none":
                print("tlevel: none")
            elif tlevel == "sentiment":
                print("tlevel: sentiment")
        else:
            print("slevel: sentiment")
            if tlevel == "none":
                print("tlevel: none")
            elif tlevel == "topic":
                print("tlevel: topic")

        return redirect(url_for('view_candidate_data', candidate_name=candidate_name))

    # first level
    elif (flevel == "topic"):
        print("flvel: topic")

        if slevel == "none":
            print("slevel: none")
        elif slevel == "candidate":
            print("slevel: candidate")

            if tlevel == "none":
                print("tlevel: none")
            elif tlevel == "sentiment":
                print("tlevel: sentiment")
        else:
            print("slevel: sentiment")
            if tlevel == "none":
                print("tlevel: none")
            elif tlevel == "candidate":
                print("tlevel: candidate")

    # first level
    else:
        print("flevel: sentiment")

        if slevel == "none":
            print("slevel: none")
        elif slevel == "candidate":
            print("slevel: candidate")

            if tlevel == "none":
                print("tlevel: none")
            elif tlevel == "topic":
                print("tlevel: topic")
        else:
            print("slevel: topic")
            if tlevel == "none":
                print("tlevel: none")
            elif tlevel == "candidate":
                print("tlevel: candidate")