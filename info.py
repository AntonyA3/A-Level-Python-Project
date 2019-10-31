
class Information:
    def __init__(self,game):
        """
        Used to store scores and player statistics
        """
        self.score=0
        self.highscore=0
        self.game=game
        self.average_score=self.game.text_files["average score"]
        self.total_bullets=0
        self.hit_bullets=0

    def game_over_routine(self):
        average_score=(int(self.average_score.read())+self.score)/2
        self.average_score.write(str(int(average_score)))
        self.game.text_files["total bullets"].write(str(int(self.game.text_files["total bullets"].read())+int(self.total_bullets)))
        self.game.text_files["hit bullets"].write(str(int(self.game.text_files["hit bullets"].read())+int(self.hit_bullets)))
        self.game.text_files["total deaths"].write(str(int(self.game.text_files["total deaths"].read())+1))
        bullet_accuracy=(float(self.game.text_files["hit bullets"].read())/float(self.game.text_files["total bullets"].read()))*100

        self.game.text_files["bullet accuracy"].write(str(bullet_accuracy))
        self.score=0
        self.total_bullets=0
        self.hit_bullets=0

   #def calc_dist_from_start

