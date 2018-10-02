import sys
import re
import intersect

# YOUR CODE GOES HERE
#Define the clase structure of database, include a name space and a coordination set x and y
class street_object:
  name =''
  vertices = []
  edges = []
  def __init__(self, name, vertices, edges):
    self.name = name          #string
    self.vertices = vertices  #point object
    self.edges = edges        #line object


#Parse the input into three parts:command, street name and coordination by xi and yi
def parse_line(line):
    
    regex = re.compile(r'''
         ".*?" | # double quoted substring
         \(.*?\) |# 
         \S+ # all the rest
         ''', re.VERBOSE)

    sp = regex.findall(line)
    #print sp
    #print 'length of sp =', len(sp)

    return (sp)

#Creat a street object
def creat_street(sp):
    numbers_rx = r'(-?[0-9]+)'
    text_rx = r'(\W)'
    i = 2
    vertices = []
    edges = []
    street_name = re.sub(text_rx,' ', sp[1]).lower()
    #print 'street name', street_name
    for i in range (2, len(sp)):
        cor = re.findall(numbers_rx, sp[i])
        if len(cor)==2:
            cor_x=int(cor[0])
            cor_y=int(cor[1])
            vertices.append(intersect.Point(cor_x, cor_y))
        else:
            return -1

    j = 0
    for j in range (0, len(vertices)-1):
        edges.append(intersect.Line(vertices[j], vertices[j+1]))


    street=street_object(street_name, vertices, edges)

    return street
    
#Manage the input into database
def db_management(sp, db_list, global_v_dic):
    command = sp[0]
    text_rx = r'(\W)'
    #print 'comand:',command

    if sp[0] == 'a': # Add a new street
        #Creat a street object
        if len(sp) > 3:
            error=creat_street(sp)
            if error == -1:
                print 'Error: Invalid input'
                return db_list, global_v_dic
            else:
                db=error
        else:
            print 'Error: Not enough input arguments'
            return db_list, global_v_dic
        #Check if there exist a street with the same street name
        j=0
        name = re.sub(text_rx,' ', sp[1]).lower()
        for j in range (0,len(db_list)):
            if db_list[j].name == name:
                print 'Error: Street exists, adding street fail'
                return db_list, global_v_dic
        #print 'New Street Name is', db.name
        #print 'New Street Vertices', db.vertices
        #print 'New Street Edges', db.edges
        #Append the new street to the database
        db_list.append(db)
    elif sp [0] == 'r': #remove a street
        #Check whether the database is empty
        if len(sp)!=2:
            print 'Error: Invalid Command'
            return db_list, global_v_dic
        if len(db_list)==0:
            print 'Error: NULL database'
            return db_list, global_v_dic


        j=0
        name = re.sub(text_rx,' ', sp[1]).lower()
        for j in range (0,len(db_list)):
            #print 'Delete Street', name
            if db_list[j].name == name:
               del db_list[j]
               #print 'Delete Successful'
               return db_list, global_v_dic
        print 'Error: No such a street to delete'
    elif sp [0] == 'c':#change a street
        if len(db_list)==0:
            print 'Error: NULL database'
            return db_list, global_v_dic

        j=0
        name = re.sub(text_rx,' ', sp[1]).lower()
        for j in range (0,len(db_list)):
            if db_list[j].name == name:
                if len(sp) > 3:
                    db_list[j]=creat_street(sp)
                    #print 'Street Updated'
                else:
                    print 'Error: Not enough input arguments'
                return db_list, global_v_dic
        print 'Error: No such a street to change'
    elif sp [0] == 'g':#generate the graph
        if len(sp)>1:
            print 'Error: Invalid Command'
            return db_list, global_v_dic
        if len(db_list)==0:
            print 'Error: NULL database'
            return db_list, global_v_dic


        #print'Generate the graph according to the present streets'
        pres_v_dic={}
        pres_e_dic=[]
        pres_v_dic,pre_e_dic,global_v_dic = intersect.generate_graph(db_list,pres_v_dic,pres_e_dic,global_v_dic)
    else: 
        print 'Error: Invalid Command'


    return db_list, global_v_dic


def main():
    ### YOUR MAIN CODE GOES HERE

    ### sample code to read from stdin.
    ### make sure to remove all spurious print statements as required
    ### by the assignment
    db_list = [] #List for storing street objects
    global_v_dic = {} #global vertices while the program running
    i = 0
    while True:
        try:
            line = sys.stdin.readline()
            if len(line) == 1:
                break
        
            #print 'read a line:', line
            #Parse and save the input
            input_data = parse_line(line)
            db_list, global_v_dic = db_management(input_data, db_list, global_v_dic)

            #for i in range (0, len(db_list)):
                #print 'street name is:', '\''+db_list[i].name+'\''
                #print 'street vertices are', db_list[i].vertices
                #print 'street edges are', db_list[i].edges
        except:
            print "Error: Invalid Input"
           

    print 'Error: No input, exit'
    # return exit code 0 on successful termination
    sys.exit(0)

if __name__ == '__main__':
    main()
