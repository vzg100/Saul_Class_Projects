import myDataModel.twit
import Classifiers.sentimentClassifier
import scala.collection.JavaConversions._
object SentinmentFinder extends App {

  val TrainReader = new reader("/Users/mark/PycharmProjects/ecigflavormining/clean_train_data.csv")
  val TestReader = new reader("/Users/mark/PycharmProjects/ecigflavormining/answers.csv")

  twit.populate(TrainReader.dataClasses.toList)
  twit.populate(TestReader.dataClasses.toList, train = false)
  sentimentClassifier.learn(2500)
  sentimentClassifier.test()
  sentimentClassifier.crossValidation(3)
  sentimentClassifier.save()
}