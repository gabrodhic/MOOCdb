require 'test_helper'

class AdminMailerTest < ActionMailer::TestCase
  test "send_admin_email" do
    mail = AdminMailer.send_admin_email
    assert_equal "Send admin email", mail.subject
    assert_equal ["to@example.org"], mail.to
    assert_equal ["from@example.com"], mail.from
    assert_match "Hi", mail.body.encoded
  end

end
