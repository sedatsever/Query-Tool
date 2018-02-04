# Query-Tool
A visual tool to simplify retrieving SQL data by generating "select" statements from user input.

# Getting Started
1. Open the "config.xml" file with a text editor like notepad. This file keeps the servers you wish to connect and their authentication information. 
2. For each server you wish to connect, fill the required data like below:

```
    <environment name="Enter your server title here">
        <server>Enter your server address here</server>
        <db>Enter a database in server here</db>
        <id>Enter user id here</id>
        <pass>Enter password here</pass>
    </environment>
```
2. Open "Query_tool.exe". 

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Sedat Sever** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
