import sys
import csv
import datetime
import time

try :
    import mechanize
    import cookielib
except:
    print "Mechanize library not installed!"
    exit()




#Define your variables here for the search
start_dob = datetime.datetime(1999, 01, 01, 00, 00, 00)      #date in (yyyy, mm, dd, hh, mm, ss)
end_dob = datetime.datetime(2000, 01, 01, 00, 00, 00)        #date in (yyyy, mm, dd, hh, mm, ss)
starting_reg_no = int(raw_input('Input starting Reg. No.: '))
ending_reg_no = int(raw_input('Input ending Reg. No.: '))
website_url = 'http://cbseresults.nic.in/class10/cbse102015_all.htm'


try :
    fp = open('results.csv','a')
    do = csv.writer(fp)
    fp.close()
except:
    print "Error in opening file!"


# Adm No. loop
while starting_reg_no <= ending_reg_no:
    reg_no = str(starting_reg_no)      
    name = ''
    
    starting_reg_no += 1
    dob = start_dob

    print '\n'
    print 'Checking for: '
    
    #DOB loop
    while dob < end_dob:

        # Browser
        br = mechanize.Browser()
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)
        br.set_handle_equiv(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_handle_refresh(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]  

        # Try to open web page
        try:
            r = br.open(website_url)
        except:
            print 'Error in reading page, please check internet connection!'
            print 'Retrying in 5 seconds ...'
            time.sleep(5)
            continue
                    

        dob_string = dob.strftime('%d/%m/%Y')
        print '[%s] of [%s] AT [%s] of [%s]' % (reg_no, str(ending_reg_no), dob_string, end_dob.strftime('%d/%m/%Y'))
        

        # Prepare form
        html = r.read()    
        br.select_form(nr = 0)
        br.form['regno'] = reg_no
        br.form['dob'] = dob_string
        
        # Try to submit form
        try:
            br.submit()
        except:
            print 'Error in submitting form, please check internet connection!'
            print 'Retrying in 5 seconds ...'
            time.sleep(5)
            continue
                    

        
        dob += datetime.timedelta(days = 1)
        page_source = br.response().read()

        ##Check if result not found
        found_index = 0
        found_index = page_source.find('Result Not Found')
        if found_index != -1:
            continue

        ##Finding user name
        name_index = 0
        name_index = page_source.find('>Name<')
        name_index = page_source.find('table_text',name_index)
        name_index += 12
        name = ''
        i=0
        while page_source[name_index+i] != '<':
            name += page_source[name_index+i]
            i += 1

        ##Finding CGPA
        cgpa_index = 0
        cgpa_index = page_source.find('CGPA')
        cgpa_index = page_source.find('<strong><strong>',cgpa_index)
        cgpa_index += 30
        result_gpa = ''
        while (page_source[cgpa_index] >= '0' and page_source[cgpa_index] <= '9') or page_source[cgpa_index] == '.':
            result_gpa += page_source[cgpa_index]
            cgpa_index += 1
            
        if result_gpa.find('.') == -1:
            result_gpa += '.0'

        # Write out the results to file
        try :
            fp = open('results.csv','a')
            do = csv.writer(fp)
            do.writerow([reg_no] + [name] + [dob_string] + [result_gpa])
            fp.close()
            print "Data written succesfully to results.csv"
        except:
            print "Error in opening file!"

        # Break DOB loop since a match was found
        break

    #DOB loop ends
#AdmNo loop ends

print '\n'
print "Finished!"
