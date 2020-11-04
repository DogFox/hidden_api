import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .models import Membership
from .models import SecretBox
from django.contrib.auth.models import User
from rest_framework_jwt.utils import jwt, jwt_payload_handler, jwt_decode_handler
from django.conf import settings

host = "smtp.gmail.com"
sender_email = "hidden.santa76@gmail.com"
ip = "95.183.35.164:8080"


def send(draft_id, *args, **kwargs):
    receivers = []
    new_users = kwargs.get('new_users')
    secretbox = SecretBox.objects.get(pk=draft_id)
    memberships_set = Membership.objects.filter(secretbox=draft_id)

    for membership in memberships_set:
        user = User.objects.get(pk=membership.member.user_id)
        payload = jwt_payload_handler(user)
        token = jwt.encode(payload, settings.SECRET_KEY)
        receiver = {'email': user.email, 'token': token.decode("utf-8")}

        if new_users:
            for new_user in new_users:
                if new_user['email'] == user.email:
                    receiver['password'] = new_user['password']

        receivers.append(receiver)

    # Сгенерировали сервер отправки
    server = smtplib.SMTP(host, 587)
    server.starttls()
    server.login(sender_email, 'afzpvkrqanqyltfa')

    for receiver in receivers:
        # Определили сообщение, при переборе будет генерить текст
        message = MIMEMultipart("alternative")

        message["Subject"] = secretbox.name + " " + secretbox.description
        message["From"] = sender_email
        message["To"] = receiver['email']

        text = """\
    Привет!
    Мы тут замутили Тайного Санту!
    Ты участвуешь!
    Переходи
    http://localhost:8080/mydrafts/""" + str(draft_id)

        htmltext = makeBodyEmail(
            draft_id, token=receiver['token'], password=receiver.get('password', None))
        # Сделать их текстовыми\html объектами MIMEText
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(htmltext, "html")

        # Внести HTML\текстовые части сообщения MIMEMultipart
        # Почтовый клиент сначала попытается отрендерить последнюю часть
        message.attach(part1)
        message.attach(part2)

        server.sendmail(sender_email, [receiver['email']], message.as_string())

    server.quit()


def makeBodyEmail(box_id, **kwargs):
    token = kwargs.get('token', '')
    password = kwargs.get('password', '')

    text = """\
                    <!DOCTYPE html
  PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office"
  style="width:100%;font-family:tahoma, verdana, segoe, sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0">

<head>
  <meta charset="UTF-8">
  <meta content="width=device-width, initial-scale=1" name="viewport">
  <meta name="x-apple-disable-message-reformatting">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta content="telephone=no" name="format-detection">
  <title>Новый шаблон 2020-10-13</title>
  <link href="https://fonts.googleapis.com/css?family=Poppins:400,700&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css?family=Poppins:400,500,600,700,900&display=swap" rel="stylesheet">
  <style type="text/css">
    #outlook a {
      padding: 0;
    }

    .ExternalClass {
      width: 100%;
    }

    .ExternalClass,
    .ExternalClass p,
    .ExternalClass span,
    .ExternalClass font,
    .ExternalClass td,
    .ExternalClass div {
      line-height: 100%;
    }

    .es-button {
      mso-style-priority: 100 !important;
      text-decoration: none !important;
    }

    a[x-apple-data-detectors] {
      color: inherit !important;
      text-decoration: none !important;
      font-size: inherit !important;
      font-family: inherit !important;
      font-weight: inherit !important;
      line-height: inherit !important;
    }

    .es-desk-hidden {
      display: none;
      float: left;
      overflow: hidden;
      width: 0;
      max-height: 0;
      line-height: 0;
      mso-hide: all;
    }

    .es-button-border:hover a.es-button {
      background: #065C66 !important;
      border-color: #065C66 !important;
    }

    .es-button-border:hover {
      border-color: #00f5f9 #00f5f9 #00f5f9 #00f5f9 !important;
      background: #065C66 !important;
    }

    @media only screen and (max-width:600px) {

      p,
      ul li,
      ol li,
      a {
        font-size: 13px !important;
        line-height: 150% !important
      }

      h1 {
        font-size: 28px !important;
        text-align: center;
        line-height: 120% !important
      }

      h2 {
        font-size: 24px !important;
        text-align: center;
        line-height: 120% !important
      }

      h3 {
        font-size: 18px !important;
        text-align: center;
        line-height: 120% !important
      }

      h1 a {
        font-size: 28px !important
      }

      h2 a {
        font-size: 24px !important
      }

      h3 a {
        font-size: 18px !important
      }

      .es-menu td a {
        font-size: 12px !important
      }

      .es-header-body p,
      .es-header-body ul li,
      .es-header-body ol li,
      .es-header-body a {
        font-size: 12px !important
      }

      .es-footer-body p,
      .es-footer-body ul li,
      .es-footer-body ol li,
      .es-footer-body a {
        font-size: 10px !important
      }

      .es-infoblock p,
      .es-infoblock ul li,
      .es-infoblock ol li,
      .es-infoblock a {
        font-size: 11px !important
      }

      *[class="gmail-fix"] {
        display: none !important
      }

      .es-m-txt-c,
      .es-m-txt-c h1,
      .es-m-txt-c h2,
      .es-m-txt-c h3 {
        text-align: center !important
      }

      .es-m-txt-r,
      .es-m-txt-r h1,
      .es-m-txt-r h2,
      .es-m-txt-r h3 {
        text-align: right !important
      }

      .es-m-txt-l,
      .es-m-txt-l h1,
      .es-m-txt-l h2,
      .es-m-txt-l h3 {
        text-align: left !important
      }

      .es-m-txt-r img,
      .es-m-txt-c img,
      .es-m-txt-l img {
        display: inline !important
      }

      .es-button-border {
        display: inline-block !important
      }

      a.es-button {
        font-size: 16px !important;
        display: inline-block !important
      }

      .es-btn-fw {
        border-width: 10px 0px !important;
        text-align: center !important
      }

      .es-adaptive table,
      .es-btn-fw,
      .es-btn-fw-brdr,
      .es-left,
      .es-right {
        width: 100% !important
      }

      .es-content table,
      .es-header table,
      .es-footer table,
      .es-content,
      .es-footer,
      .es-header {
        width: 100% !important;
        max-width: 600px !important
      }

      .es-adapt-td {
        display: block !important;
        width: 100% !important
      }

      .adapt-img {
        width: 100% !important;
        height: auto !important
      }

      .es-m-p0 {
        padding: 0px !important
      }

      .es-m-p0r {
        padding-right: 0px !important
      }

      .es-m-p0l {
        padding-left: 0px !important
      }

      .es-m-p0t {
        padding-top: 0px !important
      }

      .es-m-p0b {
        padding-bottom: 0 !important
      }

      .es-m-p20b {
        padding-bottom: 20px !important
      }

      .es-mobile-hidden,
      .es-hidden {
        display: none !important
      }

      tr.es-desk-hidden,
      td.es-desk-hidden,
      table.es-desk-hidden {
        width: auto !important;
        overflow: visible !important;
        float: none !important;
        max-height: inherit !important;
        line-height: inherit !important
      }

      tr.es-desk-hidden {
        display: table-row !important
      }

      table.es-desk-hidden {
        display: table !important
      }

      td.es-desk-menu-hidden {
        display: table-cell !important
      }

      table.es-table-not-adapt,
      .esd-block-html table {
        width: auto !important
      }

      table.es-social {
        display: inline-block !important
      }

      table.es-social td {
        display: inline-block !important
      }
    }
  </style>
</head>

<body
  style="width:100%;font-family:tahoma, verdana, segoe, sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0">
  <div class="es-wrapper-color" style="background-color:#F6F6F6">
    <table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0"
      style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-repeat:repeat;background-position:center top">
      <tr style="border-collapse:collapse">
        <td valign="top" style="padding:0;Margin:0">
          <table cellpadding="0" cellspacing="0" class="es-content" align="center"
            style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
            <tr style="border-collapse:collapse">
              <td align="center" bgcolor="#1b142d" style="padding:0;Margin:0;background-color:#1B142D">
                <table bgcolor="transparent" class="es-content-body" align="center" cellpadding="0" cellspacing="0"
                  style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
                  <tr style="border-collapse:collapse">
                    <td align="left"
                      style="Margin:0;padding-left:10px;padding-right:10px;padding-bottom:15px;padding-top:20px">
                      <table class="es-left" cellspacing="0" cellpadding="0" align="left"
                        style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left">
                        <tr style="border-collapse:collapse">
                          <td align="left" style="padding:0;Margin:0;width:280px">
                            <table width="100%" cellspacing="0" cellpadding="0" role="presentation"
                              style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                              <tr style="border-collapse:collapse">
                                <td class="es-infoblock es-m-txt-c" align="left"
                                  style="padding:0;Margin:0;line-height:14px;font-size:12px;color:#CCCCCC">
                                  <p
                                    style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:12px;font-family:tahoma, verdana, segoe, sans-serif;line-height:14.4px;color:#CCCCCC">
                                    Тсссс, никому не говори...<br></p>
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </table>
                      <table class="es-right" cellspacing="0" cellpadding="0" align="right"
                        style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:right">
                        <tr style="border-collapse:collapse">
                          <td align="left" style="padding:0;Margin:0;width:280px">
                            <table width="100%" cellspacing="0" cellpadding="0" role="presentation"
                              style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                              <tr style="border-collapse:collapse">
                                <td align="right" class="es-infoblock es-m-txt-c"
                                  style="padding:0;Margin:0;line-height:14px;font-size:12px;color:#CCCCCC">
                                  <p
                                    style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:12px;font-family:tahoma, verdana, segoe, sans-serif;line-height:14px;color:#CCCCCC">
                                    <br></p>
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
          <table cellpadding="0" cellspacing="0" class="es-content" align="center"
            style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%">
            <tr style="border-collapse:collapse">
              <td align="center" bgcolor="#1b142d" style="padding:0;Margin:0;background-color:#1B142D">
                <table bgcolor="transparent" class="es-content-body" align="center" cellpadding="0" cellspacing="0"
                  style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
                  <tr style="border-collapse:collapse">
                    <td align="left" bgcolor="#C1272C"
                      style="padding:0;Margin:0;padding-top:20px;padding-left:20px;padding-right:20px;background-color:#C1272C">
                      <table cellpadding="0" cellspacing="0" width="100%"
                        style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                        <tr style="border-collapse:collapse">
                          <td align="left" style="padding:0;Margin:0;width:560px">
                            <table cellpadding="0" cellspacing="0" width="100%" role="presentation"
                              style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                              <tr style="border-collapse:collapse">
                                <td align="center" style="padding:0;Margin:0">
                                  <h1
                                    style="Margin:0;line-height:49px;mso-line-height-rule:exactly;font-family:georgia, times, 'times new roman', serif;font-size:49px;font-style:normal;font-weight:bold;color:#333333">
                                    Тайный Санта 2020</h1>
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                  <tr style="border-collapse:collapse">
                    <td align="left" style="padding:0;Margin:0">
                      <table cellpadding="0" cellspacing="0" width="100%"
                        style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                        <tr style="border-collapse:collapse">
                          <td align="center" valign="top" style="padding:0;Margin:0;width:600px">
                            <table cellpadding="0" cellspacing="0" width="100%" role="presentation"
                              style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                              <tr style="border-collapse:collapse">
                                <td align="center" style="padding:0;Margin:0;font-size:0"><img class="adapt-img"
                                    src="https://obiens.stripocdn.email/content/guids/CABINET_5869a4dd1f7397413f5dea5ade765cb7/images/31421575535705576.png"
                                    alt
                                    style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"
                                    width="600"></td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                  <tr style="border-collapse:collapse">
                    <td align="left" bgcolor="#ffffff"
                      style="Margin:0;padding-top:20px;padding-left:20px;padding-right:20px;padding-bottom:30px;background-color:#FFFFFF">
                      <table cellpadding="0" cellspacing="0" width="100%"
                        style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                        <tr style="border-collapse:collapse">
                          <td align="left" class="es-m-p20b" style="padding:0;Margin:0;width:560px">
                            <table cellpadding="0" cellspacing="0" width="100%" role="presentation"
                              style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                              <tr style="border-collapse:collapse">
                                <td align="center" style="padding:0;Margin:0;padding-bottom:5px">
                                  <h4
                                    style="Margin:0;line-height:120%;mso-line-height-rule:exactly;font-family:Poppins, sans-serif;color:#00413F">
                                    Короче, Санта, я&nbsp;тебя спас и&nbsp;в благородство&nbsp;играть не&nbsp;буду:
                                    выполнишь для&nbsp;меня пару заданий — и&nbsp;мы в&nbsp;расчете. Заодно посмотрим,
                                    как&nbsp;быстро у&nbsp;тебя башка после бухача прояснится. А&nbsp;по твоей теме
                                    постараюсь разузнать. Хрен его&nbsp;знает, на&nbsp;кой ляд&nbsp;тебе этот "Тайный
                                    Санта"&nbsp;сдался, но&nbsp;я в&nbsp;чужие дела не&nbsp;лезу, хочешь подарить,
                                    значит есть кому...</h4>
                                </td>
                              </tr>
                              <tr style="border-collapse:collapse">
                                <td align="center"
                                  style="Margin:0;padding-left:5px;padding-right:5px;padding-top:10px;padding-bottom:10px">
                                  <p
                                    style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:15px;font-family:tahoma, verdana, segoe, sans-serif;line-height:23px;color:#333333">
                                    <br></p>
                                </td>
                              </tr>
                              """ + ("""
                              <tr style="border-collapse:collapse">
                                <td align="center" style="padding:0;Margin:0;padding-bottom:5px">
                                  <h4
                                    style="Margin:0;line-height:120%;mso-line-height-rule:exactly;font-family:Poppins, sans-serif;color:#00413F">
                                    Так как ты у нас новенький, выдам тебе временный пароль, поменять не забудь: """ + str(password) + """
                                  </h4>
                                </td>
                              </tr>
                              """ if password else """ """) + """
                              <tr style="border-collapse:collapse">
                                <td align="center"
                                  style="Margin:0;padding-left:5px;padding-right:5px;padding-top:10px;padding-bottom:10px">
                                  <p
                                    style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:15px;font-family:tahoma, verdana, segoe, sans-serif;line-height:23px;color:#333333">
                                    <br></p>
                                </td>
                              </tr>
                              <tr style="border-collapse:collapse">
                                <td align="center" style="padding:0;Margin:0;padding-bottom:10px;padding-top:15px">
                                  <span class="msohide es-button-border"
                                    style="border-style:solid;border-color:#00C4C6;background:#00413F;border-width:0px;display:inline-block;border-radius:5px;width:auto;mso-hide:all"><a
                                      href="http://""" + str(ip)+"""/mydrafts/""" + str(box_id) + """?token=""" + str(token) + """" class="es-button" target="_blank"
                                      style="mso-style-priority:100 !important;text-decoration:none;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:arial, 'helvetica neue', helvetica, sans-serif;font-size:20px;color:#FFFFFF;border-style:solid;border-color:#00413F;border-width:10px 20px 10px 20px;display:inline-block;background:#00413F;border-radius:5px;font-weight:normal;font-style:normal;line-height:24px;width:auto;text-align:center">Жмяк
                                      ➝</a>
                                  </span>
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
          <table cellpadding="0" cellspacing="0" class="es-footer" align="center"
            style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:transparent;background-repeat:repeat;background-position:center top">
            <tr style="border-collapse:collapse">
              <td align="center" bgcolor="#1b142d" style="padding:0;Margin:0;background-color:#1B142D">
                <table bgcolor="#ffffff" class="es-footer-body" align="center" cellpadding="0" cellspacing="0"
                  style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#C1272C;width:600px">
                  <tr style="border-collapse:collapse">
                    <td align="left" bgcolor="transparent"
                      style="Margin:0;padding-bottom:10px;padding-top:15px;padding-left:20px;padding-right:20px;background-color:transparent">
                      <table class="es-left" cellspacing="0" cellpadding="0" align="left"
                        style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left">
                        <tr style="border-collapse:collapse">
                          <td class="es-m-p20b" align="left" style="padding:0;Margin:0;width:270px">
                            <table width="100%" cellspacing="0" cellpadding="0" role="presentation"
                              style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                              <tr style="border-collapse:collapse">
                                <td align="left" class="es-m-txt-c" style="padding:0;Margin:0"><br></td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </table>
                      <table class="es-right" cellspacing="0" cellpadding="0" align="right"
                        style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:right">
                        <tr style="border-collapse:collapse">
                          <td align="left" style="padding:0;Margin:0;width:270px">
                            <table width="100%" cellspacing="0" cellpadding="0" role="presentation"
                              style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                              <tr style="border-collapse:collapse">
                                <td align="right" class="es-m-txt-c" style="padding:0;Margin:0">
                                  <p
                                    style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:14px;font-family:tahoma, verdana, segoe, sans-serif;line-height:21px;color:#FFFFFF">
                                    © All Rights Reserved Сучечки,&nbsp;2019</p>
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </div>
</body>

</html>
                      """
    return text
