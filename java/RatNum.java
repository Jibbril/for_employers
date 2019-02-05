// Assignment for a course at Chalmers. Builds a class called RatNum
// that does basic math with ratioal numbers.

/**
* Den här klassen hanterar grundläggande funktionalitet för 
* rationella tal som addition, subtraktion och enklare former
* jämförelser för dessa.
*
* @author  Jibbril Ndaw Berbres
* @version 153654.0
* @since   2018-12-30 
*/


public class RatNum {
  private int numerator;
  private int denominator;

  public static void main(String[] args) {
    // RatNum ratnum = new RatNum(4,8);
    // RatNum ratnum2 = new RatNum(1,2);

    // if (ratnum.hashCode() == ratnum2.hashCode()) {
    //   System.out.println("Det funkade!");
    // }
  }


  //#region Constructors
  RatNum() {
    this.numerator = 0;
    this.denominator = 1;
  }

  RatNum(int a) {
    this.numerator = a;
    this.denominator = 1;
  }

  RatNum(String s) {
    RatNum ratNum = parse(s);
    this.numerator = ratNum.getNumerator();
    this.denominator = ratNum.getDenominator();
  }

  RatNum(RatNum r) {
    this.numerator = r.getNumerator();
    this.denominator = r.getDenominator();
  }
  
  RatNum(int a, int b) {
    if (b == 0) {
      throw new NumberFormatException("Denominator = 0");  
    }

    int[] nums;
    if (a == 0) {
      nums = new int[] {0,1};
    } else {
      nums = shorten(a, b);
    }

    this.numerator = nums[0];
    this.denominator = nums[1];
  }

  //#endregion

  //#region Class methods
  /**
   * shorten(a,b) tar in två ints som tillsammans bildar ett
   * rationellt tal och förkortar sedan detta till sin enklaste
   * form (4/6 blir 2/3).
   * @param a int, täljaren i bråket
   * @param b int, nämnaren i bråket
   * @return returnar en int[] med två element där det första
   * motsvarar täljaren i det förkortade bråket och det andra nämnaren.
   */
  public static int[] shorten(int a, int b) {
    int common = 0;
    int i = 0;

    if (b < 0) {
        a = -a;
        b = -b;
    } 

    while (common != 1 && i < 2000) {
      common = gcd(a, b);
      a = a/common;
      b = b/common;
      i = i + 1;
    }
    
    int[] nums = new int[2];
    nums[0] = a;
    nums[1] = b;

    return nums;
  }

   /**
   * gcd tar in två ints och beräknar deras minsta gemensamma nämnare.
   * @param m int, täljaren i bråket
   * @param n int, nämnaren i bråket
   * @return returnar den minsta gemensamma nämnaren
   */
  public static int gcd(int m,int n) {
    if (m == 0) {
      throw new IllegalArgumentException("Numerator = 0");
    }
    if (n == 0) {
      throw new IllegalArgumentException("Denominator = 0");  
    }

    m = Math.abs(m);
    n = Math.abs(n);

    int i = 1;
    while (true && i <= 200) {
      int r = m % n;
      if (r == 0) {
        break;
      } else {
        m = n;
        n = r;
      }

      i = i + 1;
    }

    return n;
  }

   /**
   * parse(s) kontrollerar s och skapar sedan ett RatNum 
   * utifrån det om s är korrekt formaterat.
   * @param s inputsträng
   * @return returnerar ett RatNum
   */
  public static RatNum parse(String s) {
    if (s.matches("(-?[0-9]+\\/-?[0-9]+)|-?[0-9]+")) {
      int[] numbers = splitString(s);
      RatNum ratNum = new RatNum(numbers[0], numbers[1]);

      return ratNum;
    } else {
      throw new NumberFormatException("Incorrect number format!");
    }
  }

  private static int[] splitString(String s) {
    String[] numbers = s.split("/");
    int[] nums = new int[2];
    nums[0] = Integer.parseInt(numbers[0]);
    
    if (numbers.length == 2) {
       nums[1] = Integer.parseInt(numbers[1]);
    } else {
      nums[1] = 1;
    }

    return nums;
    
  }
  //#endregion
  
  //#region Instance methods
  public int getNumerator() {
    return this.numerator;
  }

  public int getDenominator() {
    return this.denominator;
  }

  public String toString() {
    return this.numerator + "/" + this.denominator;
  }

  public double toDouble() {
    return (double) this.numerator / (double) this.denominator;
  }

  public Object clone() {
    return new RatNum(this.numerator, this.denominator);
  }

  public void printNums() {
    System.out.println("Numerator: " + this.numerator);
    System.out.println("Denominator: " + this.denominator);
  }

  public boolean equals(Object o) {
    if (o instanceof RatNum) {
      RatNum r = RatNum.class.cast(o);
      return this.numerator == r.getNumerator() && this.denominator == r.getDenominator();
    } else {
      return false;
    }
  }

  public boolean lessThan(RatNum r) {
    return this.toDouble() < r.toDouble();
  }

  public RatNum add(RatNum r) {
    int a = this.getNumerator();
    int b = this.getDenominator();
    int c = r.getNumerator();
    int d = r.getDenominator();

    return new RatNum((a*d + b*c), b*d);
  }

  public RatNum sub(RatNum r) {
    int a = this.getNumerator();
    int b = this.getDenominator();
    int c = r.getNumerator();
    int d = r.getDenominator();

    return new RatNum((a*d - b*c), b*d);
  }

  public RatNum mul(RatNum r) {
    int a = this.getNumerator();
    int b = this.getDenominator();
    int c = r.getNumerator();
    int d = r.getDenominator();

    return new RatNum(a*c, b*d);
  }

  public RatNum div(RatNum r) {
    int a = this.getNumerator();
    int b = this.getDenominator();
    int c = r.getNumerator();
    int d = r.getDenominator();

    return new RatNum(a*d, b*c);
  }

  public int hashCode() {
    int hash1 = 7;
    int hash2 = 31;

    if (this.numerator == 0) {
      return 0;
    } else {
      int[] nums = RatNum.shorten(this.numerator, this.denominator);
      return nums[0] * hash1 + nums[1] * hash2;
    }
  }

  //#endregion

}
