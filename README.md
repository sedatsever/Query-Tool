# Query-Tool
A visual tool to simplify retrieving SQL data by generating "select" statements from user input.

# Getting Started
1. Open the "config.xml" file with a text editor like notepad. This file keeps the servers you wish to connect and their authentication information. 
2. For each server you wish to connect, you need to insert a block like below into the config.xml. Fill the required fields as stated below:

```
    <environment name="Enter your server title in double quotes here">
        <server>Enter your server address here</server>
        <db>Enter a database in server here</db>
        <id>Enter user id here</id>
        <pass>Enter password here</pass>
    </environment>
```
Note: Only use English characters in config file

# Manual
1. Open "Query_tool.exe"
2. First select a server from the "Servers" combo box. You have to click on a server to connect and list databases.
3. When you successfully connect to the server, databases are listed on the right. Select a database and click on connect button.
4. When you are connected to the database, you may directly write your sql statement in the "Query" box and hit "Run" to retrieve data.
5. You may also use the generate feature. To do so, select a table, column, operator and enter criteria. The sql staement will be automatically generated in the query box.
6. You may right click on the table to copy data or headers.

## Built With
* [Python](https://www.python.org/) - Coding language
* [Pyodbc](https://github.com/mkleehammer/pyodbc) - The sql framework used
* [Pyqt5](https://riverbankcomputing.com/software/pyqt/intro) - Used fur UI
* [ElementTree](https://docs.python.org/2/library/xml.etree.elementtree.html) - Used for xml

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Author

* **Sedat Sever** - *Initial work* - [sedatsever](https://github.com/sedatsever)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* The author will not be held responsible for any damage caused by using this software.
