#!/usr/bin/env python
import re, libsbml, numpy, sys, validatorSBtab

def validateSBtab(tabFile, reportFile):
  def_table = open('definitions.csv','r')
  definitions = def_table.read()
  def_table.close()
  
  file = open(tabFile,'r')
  document = file.read();
  file.close();
  
  numErrors = 0
  messages = []
  result = {}
  try: 
    validate = validatorSBtab.ValidateTable(document,tabFile,definitions,'./definitions.csv')
    result = validate.returnOutput()
  except Exception, e: 
    messages.append(str(e))
    numErrors = numErrors + 1
  
  for tag in result: 
    table = tag[tag.rfind('_')+1:]
    log = result[tag]
    numErrors = numErrors + len(log)
    if len(log) > 0: 
       messages.append('Errors in {0} table:'.format(table))
       messages.append('  ')
       for item in log: 
         for entry in item:
           messages.append('  {0}'.format(entry))
  
  if numErrors == 0:
    messages.insert(0, '')
    messages.insert(0, 'This is a valid SBtab description.')
  else: 
    messages.insert(0, '')
    messages.insert(0, 'The table contains {0} error(s).'.format(numErrors))
  
  log = open(reportFile,'w')
  for item in messages: 
    log.write(item + '\n');
   
  log.close();

if __name__ == '__main__':
  validateSBtab(sys.argv[1],sys.argv[2])
