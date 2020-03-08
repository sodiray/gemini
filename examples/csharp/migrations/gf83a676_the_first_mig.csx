#r "nuget: RestSharp, 106.10.1"

using RestSharp;

const string version = "gf83a676";
const string parent = null;
const string name = "the_first_mig";

public static void Up()
{
    Console.WriteLine("Running up migration");
    Console.WriteLine(typeof(RestClient));
}

public static void Down()
{
    Console.WriteLine("Running down migration");
}
