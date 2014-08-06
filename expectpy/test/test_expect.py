import unittest
from expectpy import expect
from expectpy.expect import assertmethod
from expectpy import __VERSION__


class TestAssertionBuilder(unittest.TestCase):

    def test_import(self):
        self.assertIsNotNone(expect)
        self.assertIsNotNone(__VERSION__)

    def test_expect_has_language_chains_attribute(self):
        expected = expect("test")
        self.assertEqual(expected.be, expected)
        self.assertEqual(expected.been, expected)
        self.assertEqual(expected.be.been, expected)
        self.assertEqual(expected.to.be, expected)
        try:
            expected.to.abcde
            self.fail()
        except AttributeError:
            pass

    def test_assertmethod_decorater_is_raise_assertion_error(self):
        class A:
            def __init__(self, negative=False):
                self.negative = negative

            @assertmethod
            def test(self):
                err = "it is custome message"
                err_not = "it is 'Not' custome message"
                return self.negative, err, err_not

        self.assertRaises(AssertionError, A().test)
        try:
            A().test()
            self.fail()
        except Exception as e:
            self.assertEqual("it is custome message", str(e))

        try:
            a = A(True)
            a.test()
            self.fail()
        except Exception as e:
            self.assertEqual("it is 'Not' custome message", str(e))

    def test_equal(self):
        try:
            expect("test").to.equal("test")
        except:
            self.fail()
        self.assertRaises(AssertionError, expect("test").to.equal, "Test")
        try:
            expect("test").to.equal("tea", "It is error message Test")
        except Exception as e:
            expect(str(e)).to.equal("It is error message Test")

        try:
            expect([]).to_not.be.equal([])
        except AssertionError as e:
            expect(str(e)).to.equal("expected [] to not equal []")

    def test_a(self):
        class A:
            pass

        expect("test").to.be.a(str)
        expect(100).to.be.a(int)
        expect({}).to.be.a(dict)
        expect([]).to.be.a(list)
        expect(A()).to.be.a(A)
        expect([]).to.be.a(list)

        self.assertRaises(AssertionError, expect([]).to.be.a, str)

        try:
            expect([]).to.be.an(int)
            self.fail()
        except AssertionError as e:
            expect(str(e)).to.equal("expected [] to be an int")

        try:
            expect([]).to_not.be.an(list)
            self.fail()
        except AssertionError as e:
            expect(str(e)).to.equal("expected [] to not be an list")

        try:
            expect([]).to.be.an(int, "Custome Message")
            self.fail()
        except AssertionError as e:
            expect(str(e)).to.equal("Custome Message")

    def test_not(self):
        expect("test").to_not.be.a(int)
        expect("test").to_not.be.not_.a(str)

    def test_ok(self):
        class A:
            pass
        expect("test").to.be.ok
        expect(1).to.be.ok
        expect(A()).to.be.ok

        expect("").to_not.be.ok
        expect(0).to_not.be.ok
        expect(None).to_not.be.ok

    def test_empty(self):
        expect([]).to.be.empty
        expect("").to.be.empty

        expect(["", ""]).to_not.be.empty
        expect("a").to_not.be.empty

    def test_be_None(self):
        expect(None).to.be_None
        expect("test").to_not.be_None

        try:
            expect(None).to_not.be._None
            self.fail()
        except:
            pass

    def test_above_and_least(self):
        expect(6).to.be.above(5)
        self.assertRaises(AssertionError, expect(5).to.be.above, 5)

        expect(1).to.be.least(1)
        self.assertRaises(AssertionError, expect(0).to.be.least, 1)

        try:
            expect(1).to.be.above(2)
            self.fail()
        except AssertionError as e:
            expect(str(e)).to.equal("expected 1 to be above 2")

        try:
            expect(1).to.be.least(2)
            self.fail()
        except AssertionError as e:
            expect(str(e)).to.equal("expected 1 to be least 2")

    def test_below_and_most(self):
        expect(5).to.be.below(6)
        expect(5).to.be.most(5)
        expect(5).to.be.most(6)

        expect(5).to_not.be.below(4)
        expect(5).to_not.be.below(5)
        expect(5).to_not.be.most(4)

    def test_throw(self):
        def raise_(err):
            raise err
        expect(lambda: raise_(ValueError())).to.throw(ValueError)
        expect(lambda: raise_(ValueError())).to_not.throw(AssertionError)
        try:
            expect(lambda: raise_(ValueError())).to.throw(AssertionError)
            self.fail()
        except AssertionError as e:
            expect(str(e)).to.equal("actual to throw AssertionError")

    def test_satisfy(self):
        expect("test").to.satisfy(lambda actual: actual == "test")
        expect("test").to_not.satisfy(lambda actual: actual == "t")

        try:
            expect("tet").to.satisfy(lambda actual: actual == "test")
            self.fail()
        except AssertionError as e:
            expect(str(e)).to.equal("expected tet to satisfy <lambda>")

    def test_within(self):
        expect(5).to.be.within(3, 6)
        expect(5).to.be.within(5, 6)
        expect(5).to.be.within(3, 5)
        expect(1).to_not.be.within(3, 5)

        try:
            expect(4).to.be.within(5, 6)
            self.fail()
        except AssertionError as e:
            expect(str(e)).to.equal("expected 4 to be within 5..6")

        try:
            expect(5).to.not_.be.within(4, 6)
            self.fail()
        except AssertionError as e:
            expect(str(e)).to.equal("expected 5 to not be within 4..6")

    def test_string(self):
        expect("foobar").to.have.string("bar")
        expect("foobar").to.have.string("foo")
        expect("foobar").to_not.have.string("baz")

        try:
            expect("foobar").to.string("bbb")
            self.fail()
        except AssertionError as e:
            expect(str(e)).to.equal("expected foobar to contain bbb")

    def test_include_and_contain(self):
        expect("foobar").to.include("bar")
        expect("foobar").to.contain("bar")

        try:
            expect("foobar").to.contain("aaa")
            self.fail()
        except AssertionError as e:
            expect(str(e)).to.eql("expected foobar to contain aaa")

    def test_match(self):
        expect("foobar").to.match(r"^foo")
        expect("foobar").to.match(r".*bar$")
        expect("foobar").to_not.match(r"tet")

        try:
            expect("foobar").to.match(r"/test")
            self.fail()
        except AssertionError as e:
            expect(str(e)).to.eql("expected foobar to match /test")

    def test_be_True(self):
        expect(True).to.be_True

    def test_be_False(self):
        expect(False).to.be_False

    def test_ownProperty(self):
        val = {"foo": "bar"}
        expect(val).to.have.ownProperty("foo")

        try:
            expect({}).to.have.ownProperty("foo")
        except AssertionError as e:
            expect(str(e)).to.eql("expected {} to have own property foo")

    def test_property_(self):
        val = {"foo": "bar"}
        expect(val).to.have.property_("foo", "bar")
        expect(val).to.have.property_("foo")

        try:
            expect({}).to.have.property_("foo")
        except AssertionError as e:
            expect(str(e)).to.equal("expected {} to have own property foo")

    def test_length(self):
        expect([1, 2, 3]).to.have.length(3)
        expect("123").to.have.length(3)

        expect("foo").to.have.length_.above(2)
        expect("foo").to.have.length_.within(2, 5)

    def test_method_chane(self):
        expect([1, 2, 3]).to_not.have.length(2).and_.length_.below(2)
