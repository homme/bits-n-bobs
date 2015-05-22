import easyimap, re, os

# Fill out IMAP login details
host = ''
user = ''
password = ''
mailbox = 'INBOX'
host = ''
port = 993
ssl = True

cre = re.compile('"/" ')

def iter_mailboxes(imapper):
    mailer = imapper._mailer
    kind, boxes = mailer.list()
    for box in (cre.split(mb)[-1] for mb in boxes):
        yield box

def iter_alluids(imapper):
    for box in iter_mailboxes(imapper):
        imapper.change_mailbox(box)
        for uid in imapper.listids(limit=-1):
            yield box, uid

def iter_mail(imapper):
    for uid in imapper.listids(limit=-1):
        mail = imapper.mail(uid, include_raw=True)
        yield mail

def iter_allmail(imapper):
    for box in iter_mailboxes(imapper):
        print "Changing to '%s'" % box
        imapper.change_mailbox(box)
        for mail in iter_mail(imapper):
            yield mail

def save_attachment(attachment):
    name, data = attachment[:2]
    save_name = name
    root, ext = os.path.splitext(name)
    count = 1
    while os.path.exists(save_name):
        save_name = os.path.extsep.join(['%s_%d' % (root, count), ext])
        count += 1

    print save_name
    with open(save_name, 'w') as f:
        f.write(data)
            
def main():
    imapper = easyimap.connect(host, user, password, mailbox, ssl, port)

    #for mail in iter_allmail(imapper):
    #    for attachment in mail.attachments:
    #        save_attachment(attachment)

    current_box = None
    for box, uid in iter_alluids(imapper):
        filename = '%s%s%s.eml' % (box, os.path.sep, uid)
        if not os.path.exists(filename):
            if current_box != box:
                print "Changing to '%s'" % box
                imapper.change_mailbox(box)
                current_box = box
                if not os.path.exists(box):
                    os.makedirs(box)

            print "Saving %s" % filename
            try:
                mail = imapper.mail(uid, include_raw=True)
            except TypeError:
                print "Cannot access %s" % filename
                continue

            with open(filename, 'w') as f:
                f.write(mail.raw)
        else:
            print "Skipping %s" % filename

    imapper.quit()
    
if __name__ == '__main__':
    main()
