require 'test_helper'

class UserMailerTest < ActionMailer::TestCase
  test "user_approved" do
    mail = UserMailer.user_approved
    assert_equal "User approved", mail.subject
    assert_equal ["to@example.org"], mail.to
    assert_equal ["from@example.com"], mail.from
    assert_match "Hi", mail.body.encoded
  end

end
