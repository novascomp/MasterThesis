import org.apache.spark.sql.{DataFrame, SparkSession, functions}

import scala.util.Try

class HSM() extends Serializable {

  val crypto = Main.initCryptoApi();
  val HSM_IV = false;

  def encrypt(id: String, colName: String, plaintext: String): String = {
    crypto.encrypt(crypto.getSecretText(), id, colName, plaintext, HSM_IV)
  }

  def decrypt(id: String, colName: String, encryptedText: String): String = {
    crypto.decrypt(crypto.getSecretText(), id, colName, encryptedText, HSM_IV)
  }
}

object HSM {
  val instance: HSM = new HSM()
}

object ScalaMain extends App {

  val NA_CHAR = "-"
  val REQUEST_ID = args.apply(0)
  val FILE_PATH = args.apply(1)
  val KEY_LABEL = args.apply(2)
  val COL_NAMES_TO_PSEUD = args.apply(3).split(",")
  val PSEUD_OPERATION = args.apply(4).toLowerCase()
  val OUTPUT_PATH = args.apply(5)
  val ID_COL_NAME = args.apply(6)
  val FORMAT = args.apply(7)
  val LIMIT = args.apply(8)
  val NUM_PARTITION = args.apply(9)

  val spark = SparkSession.builder().appName(REQUEST_ID).getOrCreate();
  val df_input: DataFrame = readInput(spark, FORMAT.toLowerCase(), FILE_PATH, NA_CHAR, LIMIT)
  val df_final = performCrypto(df_input, PSEUD_OPERATION.toLowerCase(), ID_COL_NAME, COL_NAMES_TO_PSEUD.toSet)
  writeOutput(FORMAT.toLowerCase(), OUTPUT_PATH, df_final)

  def tryToInt(s: String) = Try(s.toInt).toOption

  private def readInput(spark: SparkSession, format: String, filePath: String, naChar: String, limit: String): DataFrame = {
    if (format == "parquet") {
      return spark.read.parquet(filePath).na.fill(naChar).limit(tryToInt(limit).get).repartition(tryToInt(NUM_PARTITION).get)
    }
    spark.read.options(Map("inferSchema" -> "true", "delimiter" -> ",", "header" -> "true")).csv(filePath).na.fill(naChar).limit(tryToInt(limit).get).repartition(tryToInt(NUM_PARTITION).get)
  }

  private def writeOutput(format: String, outputPath: String, df_final: DataFrame): Unit = {
    if (format == "parquet") {
      df_final.write.mode("overwrite").option("header", true).parquet(outputPath)
    } else {
      df_final.coalesce(1).write.mode("overwrite").option("header", true).csv(outputPath)
    }
  }

  private def performCrypto(df_input: DataFrame, pseudOperation: String, idColName: String, colNamesToPseud: Set[String]): DataFrame = {
    val pseud_hsm = (id: String, colName: String, plainText: String) => {
      HSM.instance.encrypt(id, colName, plainText)
    }

    val de_pseud_hsm = (id: String, colName: String, encryptedText: String) => {
      HSM.instance.decrypt(id, colName, encryptedText)
    }

    val pseud_udf = functions.udf(pseud_hsm)
    val de_pseud_udf = functions.udf(de_pseud_hsm)

    val plain_cols = df_input.columns.filterNot(colNamesToPseud)
    if (pseudOperation.toLowerCase() == "pseud") {
      //different approach
      //return colNamesToPseud.toList.par.foldLeft(df_input) { (tempdf, colName) =>
      //  tempdf.withColumn(colName, pseud_udf(functions.col(idColName), functions.lit(colName), functions.col(colName)))
      //}

      return df_input.select((plain_cols.map(col_name => functions.col(col_name)) ++ colNamesToPseud.map(colName => pseud_udf(functions.col(idColName), functions.lit(colName), functions.col(colName)).alias(colName))): _*)
    }
    df_input.select(plain_cols.map(col_name => functions.col(col_name)) ++ colNamesToPseud.map(colName => de_pseud_udf(functions.col(idColName), functions.lit(colName), functions.col(colName)).alias(colName)): _*)
  }
}