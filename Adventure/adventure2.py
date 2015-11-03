rooms = [ "Βρισκεσαι στον κήπο. Παντού σκοτάδι.",
          "Βρίσκεσαι στο μπάνιο. Ακούς θόρυβο.",
          "Βρίσκεσαι στο χωλ. Παραλίγο να σκοντάψεις. Σκάλα ανατολικά",
          "Βρισκεσαι στην αποθήκη. Η ατμόσφαιρα είναι αποπνικτική. Σκάλα Δυτικά, Μονοπάτι Νότια.",
          "Έφτασες στο καθιστικό. Βρήκες τον πατέρα σου.",
          "Βρίσκεσαι στο σαλόνι. Ακούγεται μουσική.",
          "Βρίσκεσαι στην τραπεζαρία. Τα πάντα είναι ανάστατα.",
          "Βρίσκεσαι στο διάδρομο. Είναι σκοτεινά. Σκάλα Νότια",
          "Είσαι στη κουζίνα. Ακούς φωνές.",
          "Είσαι στον πάνω διάδρομο. Παντού ησυχία. Σκάλα Βόρεια.",
          "Είσαι στο δωμάτιο του αδερφού σου. Ο αδερφός σου σε μαρτυρά!",
          "Είσαι στο δωμάτιο των γονέων σου. Η μητέρα σου σε έπιασε.",
          "Είσαι στο δωμάτιο σου. Είσαι ασφαλής." ]

moves = [   [-1,2,-1,-1],
            [-1,-1,2,-1],
            [0,5,3,1],
            [-1,8,-1,2],
            [-1,6,5,-1],
            [2,8,-1,4],
            [4,7,-1,-1],
            [6,9,8,-1],
            [5,-1,-1,7],
            [7,11,12,10],
            [-1,-1,9,-1],
            [9,-1,-1,-1],
            [-1,-1,-1,9] ]
 
winrooms = [ 12 ]

lossrooms = [ 4, 10, 11 ]
directions = [ "Βόρεια","Νότια","Ανατολικά","Δυτικά"]

room = 0
game = True
while game:
    print rooms [room]
    if room in winrooms:
        print "Kerdises"
        game = False
    elif room in lossrooms:
        print "Exases"
        game = False
    else:
        exits = moves [room]
        print "0 = Βόρεια, 1 = Νότια, 2 = Ανατολικα, 3 = Δυτικά"
        index = 0
        for i in exits:
            if i!=-1:
                print directions[index]
            index = index + 1
        choice = input ("Direction:")
        while exits[choice]==-1:
          choice = input ("Direction:")
        room = exits [choice]

